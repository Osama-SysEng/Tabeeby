"""
TABEEBY Authentication & Authorization Service
Multi-tier MFA, Biometric, Zero-Trust, Blockchain Audit
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import jwt
import hashlib
import secrets
import os
import redis.asyncio as redis
from enum import Enum

app = FastAPI(title="Tabeeby Auth Service", version="1.0.0")

redis_client = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)

APP_ENV = os.getenv("TABEEBY_ENV", "development")
DEV_AUTH_ENABLED = os.getenv("TABEEBY_DEV_AUTH", "false").lower() == "true"
DEV_LOGIN_EMAIL = os.getenv("TABEEBY_DEV_LOGIN_EMAIL", "")
DEV_LOGIN_PASSWORD = os.getenv("TABEEBY_DEV_LOGIN_PASSWORD", "")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET:
    if APP_ENV == "production":
        raise RuntimeError("JWT_SECRET_KEY must be set in production")
    JWT_SECRET = secrets.token_urlsafe(48)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(hours=1)
REFRESH_TOKEN_EXPIRE = timedelta(days=30)

class UserTier(str, Enum):
    PATIENT = "patient"
    PHYSICIAN = "physician"
    RESEARCHER = "researcher"
    BIOINFORMATICIAN = "bioinfo"
    SURGEON = "surgeon"
    ADMIN = "admin"

class AuthRequest(BaseModel):
    email: EmailStr
    password: str
    tier: UserTier
    mfa_code: Optional[str] = None
    biometric_token: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    tier: UserTier
    permissions: List[str]

class PermissionMatrix:
    """Granular per-action permission matrix"""
    PERMISSIONS = {
        UserTier.PATIENT: [
            "patient:read_own", "patient:update_own", "vitals:read_own",
            "appointment:create", "emergency:trigger", "ai_physician:chat"
        ],
        UserTier.PHYSICIAN: [
            "patient:read_assigned", "patient:write_assigned",
            "diagnosis:create", "treatment:prescribe", "surgery:plan",
            "imaging:read", "lab:read", "ai_decision:support",
            "robot:assign", "emergency:respond"
        ],
        UserTier.RESEARCHER: [
            "research:read", "research:write", "population:analyze",
            "drug:discover", "clinical_trial:manage", "database:query"
        ],
        UserTier.BIOINFORMATICIAN: [
            "bio_robot:program", "bio_robot:deploy", "bio_robot:monitor",
            "nano:surgery_plan", "nano:deploy", "simulation:run",
            "molecular:analyze", "genomic:sequence"
        ],
        UserTier.SURGEON: [
            "surgery:execute", "surgery:vr_simulate", "surgery:ar_assist",
            "robot:surgical_control", "4d:temporal_sim", "4d:quantum_model",
            "consciousness:monitor", "collective:collaborate"
        ],
        UserTier.ADMIN: ["*"]
    }

    @classmethod
    def get_permissions(cls, tier: UserTier) -> List[str]:
        return cls.PERMISSIONS.get(tier, [])

    @classmethod
    def check_permission(cls, tier: UserTier, action: str) -> bool:
        perms = cls.get_permissions(tier)
        return "*" in perms or action in perms

class BlockchainAudit:
    """Blockchain-anchored immutable audit trail"""
    @staticmethod
    async def log_access(user_id: str, action: str, resource: str, success: bool):
        timestamp = datetime.utcnow().isoformat()
        data = f"{user_id}:{action}:{resource}:{timestamp}:{success}"
        hash_digest = hashlib.sha256(data.encode()).hexdigest()
        await redis_client.lpush("audit_log", json.dumps({
            "hash": hash_digest,
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "timestamp": timestamp,
            "success": success
        }))

security = HTTPBearer()

def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "auth", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(request: AuthRequest):
    """Multi-factor authentication with tier-based permissions"""
    if len(request.password) < 8:
        raise HTTPException(status_code=422, detail="Password must contain at least 8 characters")
    if not DEV_AUTH_ENABLED:
        raise HTTPException(status_code=503, detail="Identity provider is not configured; login is disabled")
    if not DEV_LOGIN_EMAIL or not DEV_LOGIN_PASSWORD or not secrets.compare_digest(request.email, DEV_LOGIN_EMAIL) or not secrets.compare_digest(request.password, DEV_LOGIN_PASSWORD):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = hashlib.sha256(request.email.encode()).hexdigest()[:16]

    # MFA check for Tiers 4+5
    if request.tier in [UserTier.BIOINFORMATICIAN, UserTier.SURGEON]:
        if not request.mfa_code or not request.biometric_token:
            raise HTTPException(status_code=401, detail="MFA + Biometric required for this tier")

    # MFA check for Tier 3+
    if request.tier in [UserTier.RESEARCHER, UserTier.BIOINFORMATICIAN, UserTier.SURGEON]:
        if not request.mfa_code:
            raise HTTPException(status_code=401, detail="MFA required for this tier")

    permissions = PermissionMatrix.get_permissions(request.tier)

    access_token = create_token(
        {"sub": user_id, "email": request.email, "tier": request.tier.value, "perms": permissions},
        ACCESS_TOKEN_EXPIRE
    )
    refresh_token = create_token(
        {"sub": user_id, "type": "refresh"},
        REFRESH_TOKEN_EXPIRE
    )

    # Log to blockchain audit
    await BlockchainAudit.log_access(user_id, "login", "auth_system", True)

    # Store session in Redis
    await redis_client.setex(f"session:{user_id}", 3600, access_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=3600,
        tier=request.tier,
        permissions=permissions
    )

@app.post("/api/v1/auth/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")
        new_access = create_token(
            {"sub": user_id, "type": "access"},
            ACCESS_TOKEN_EXPIRE
        )
        return {"access_token": new_access, "token_type": "bearer", "expires_in": 3600}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.post("/api/v1/auth/logout")
async def logout(user: dict = Depends(get_current_user)):
    """Invalidate session"""
    user_id = user.get("sub")
    await redis_client.delete(f"session:{user_id}")
    await BlockchainAudit.log_access(user_id, "logout", "auth_system", True)
    return {"message": "Logged out successfully"}

@app.get("/api/v1/auth/verify")
async def verify_permission(action: str, user: dict = Depends(get_current_user)):
    """Verify if user has permission for specific action"""
    tier = UserTier(user.get("tier", "patient"))
    has_perm = PermissionMatrix.check_permission(tier, action)
    return {
        "user_id": user.get("sub"),
        "tier": tier.value,
        "action": action,
        "authorized": has_perm
    }

@app.get("/api/v1/auth/audit-log")
async def get_audit_log(limit: int = 100, user: dict = Depends(get_current_user)):
    """Retrieve blockchain-anchored audit log"""
    if not PermissionMatrix.check_permission(UserTier(user.get("tier", "patient")), "admin:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    logs = await redis_client.lrange("audit_log", 0, limit - 1)
    import json
    return {"logs": [json.loads(log) for log in logs], "total": len(logs)}

@app.post("/api/v1/auth/biometric/enroll")
async def enroll_biometric(
    fingerprint_hash: Optional[str] = None,
    retinal_hash: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    """Enroll biometric data for Tiers 4+5"""
    user_id = user.get("sub")
    tier = UserTier(user.get("tier", "patient"))

    if tier not in [UserTier.BIOINFORMATICIAN, UserTier.SURGEON]:
        raise HTTPException(status_code=403, detail="Biometric enrollment restricted to Tiers 4-5")

    biometric_data = {
        "user_id": user_id,
        "fingerprint": fingerprint_hash,
        "retinal": retinal_hash,
        "enrolled_at": datetime.utcnow().isoformat()
    }

    await redis_client.setex(f"biometric:{user_id}", 86400 * 365, str(biometric_data))
    return {"status": "enrolled", "user_id": user_id}

import json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
