"""
TABEEBY API Gateway
Central routing, rate limiting, auth, and request distribution
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import asyncio
import redis.asyncio as redis
from typing import Optional
import jwt
from datetime import datetime
import uuid
import os
import sys
from pathlib import Path

# Make the shared defensive package available both locally and in the image.
_shared_root = str(Path(__file__).resolve().parents[1])
if _shared_root not in sys.path:
    sys.path.insert(0, _shared_root)
from shared.security.ip_policy import parse_networks, resolve_client_ip
from shared.security.monitoring import make_security_event
from shared.security.detection import DetectionEngine

app = FastAPI(title="Tabeeby API Gateway", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

# Redis for rate limiting & caching
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Service URLs
SERVICES = {
    "auth": "http://auth-service:8002",
    "patient": "http://patient-service:8003",
    "physician": "http://physician-service:8004",
    "diagnostic": "http://diagnostic-ai:8005",
    "drug": "http://drug-discovery:8006",
    "bio": "http://bio-robot-os:8007",
    "nano": "http://nano-os:8008",
    "surgical": "http://surgical-4d:8009",
    "robot": "http://robot-os:8010",
    "iot": "http://iot-service:8011",
    "emergency": "http://emergency-service:8012",
    "research": "http://research-service:8013",
    "national": "http://national-health:8014",
    "notification": "http://notification-service:8015",
    "billing": "http://billing-service:8016",
    "file-security": "http://file-security:8017",
    "ultra-iq": "http://ultra-iq-engine:8001",
}

# JWT Config
APP_ENV = os.getenv("TABEEBY_ENV", "development")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET:
    if APP_ENV == "production":
        raise RuntimeError("JWT_SECRET_KEY must be set in production")
    JWT_SECRET = "development-only-insecure-secret-change-me"
JWT_ALGORITHM = "HS256"
MAX_BODY_BYTES = int(os.getenv("MAX_BODY_BYTES", "1048576"))
TRUSTED_PROXY_CIDRS = tuple(filter(None, os.getenv("TRUSTED_PROXY_CIDRS", "").split(",")))
parse_networks(TRUSTED_PROXY_CIDRS)
detection_engine = DetectionEngine()

async def verify_token(request: Request) -> dict:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        print(make_security_event("auth.failure", "denied", request_id=getattr(request.state, "request_id", None), client_ip=getattr(request.state, "client_ip", None), details={"reason": "missing_bearer"}).to_json())
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        token = auth.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print(make_security_event("auth.failure", "denied", request_id=getattr(request.state, "request_id", None), client_ip=getattr(request.state, "client_ip", None), details={"reason": "expired_token"}).to_json())
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        print(make_security_event("auth.failure", "denied", request_id=getattr(request.state, "request_id", None), client_ip=getattr(request.state, "client_ip", None), details={"reason": "invalid_token"}).to_json())
        raise HTTPException(status_code=401, detail="Invalid token")

async def rate_limit_check(user_id: str, tier: str = "standard"):
    """Rate limiting based on user tier"""
    limits = {"patient": 100, "physician": 1000, "researcher": 5000, 
              "bioinfo": 10000, "surgeon": 20000, "admin": 100000}
    limit = limits.get(tier, 100)
    key = f"rate_limit:{user_id}"
    current = await redis_client.incr(key)
    if current == 1:
        await redis_client.expire(key, 60)
    if current > limit:
        print(make_security_event("rate.limit.exceeded", "denied", details={"subject": user_id, "tier": tier, "limit": limit}).to_json())
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_BODY_BYTES:
        return JSONResponse(status_code=413, content={"detail": "Request body too large", "request_id": request_id})

    peer_ip = request.client.host if request.client else "0.0.0.0"
    forwarded_for = request.headers.get("x-forwarded-for")
    try:
        request.state.client_ip = resolve_client_ip(peer_ip, forwarded_for, TRUSTED_PROXY_CIDRS)
    except ValueError:
        # Non-IP peers (e.g. Starlette TestClient "testclient"): use raw value, trust nothing.
        request.state.client_ip = peer_ip

    # Log only metadata; never log query strings, authorization, or clinical payloads.
    print(f"[{datetime.utcnow().isoformat()}] {request_id} {request.method} {request.url.path} client={request.state.client_ip}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.get("/health")
async def health_check():
    """Gateway health check"""
    return {
        "status": "healthy",
        "gateway": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.1.0",
        "mode": "simulation_only" if APP_ENV != "production" else "production"
    }

@app.get("/api/v1/services/status")
async def services_status():
    """Check all microservices health"""
    statuses = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in SERVICES.items():
            try:
                resp = await client.get(f"{url}/health")
                statuses[name] = {"status": "up", "code": resp.status_code}
            except:
                statuses[name] = {"status": "down", "code": 0}
    return statuses

# Dynamic route proxy
@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(
    service: str,
    path: str,
    request: Request,
    user: dict = Depends(verify_token)
):
    """Proxy requests to appropriate microservice"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service {service} not found")

    await rate_limit_check(user.get("sub"), user.get("tier", "standard"))

    target_url = f"{SERVICES[service]}/api/v1/{path}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        method = request.method
        headers = dict(request.headers)
        for header in ("host", "authorization", "x-forwarded-for", "x-real-ip", "forwarded"):
            headers.pop(header, None)
        headers["x-gateway-user-id"] = str(user.get("sub", ""))
        headers["x-gateway-user-tier"] = str(user.get("tier", "standard"))

        body = await request.body()
        if len(body) > MAX_BODY_BYTES:
            raise HTTPException(status_code=413, detail="Request body too large")

        try:
            response = await client.request(
                method=method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text},
                status_code=response.status_code
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service unavailable")

# WebSocket upgrade for real-time services
@app.websocket("/ws/{service}")
async def websocket_proxy(websocket, service: str):
    """WebSocket proxy for real-time services (IoT, vitals, surgical)"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Route to appropriate service
            await websocket.send_json({"ack": True, "service": service, "data": data})
    except:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
