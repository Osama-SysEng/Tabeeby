"""Tabeeby Edge Computing Service - offline-capable sync node registry (simulation-only mocks)."""
from datetime import datetime, timezone
import random
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tabeeby Edge Computing Service", version="1.0.0")

SERVICE_NAME = "edge-computing"
VERSION = "1.0.0"
DISCLAIMER = (
    "Simulation-only mock data for development and testing. "
    "No real devices are contacted."
)

db: dict = {}

EDGE_NODES = [
    {"node_id": "cairo-edge-1", "region": "cairo", "status": "online", "offline_capable": True},
    {"node_id": "alexandria-edge-2", "region": "alexandria", "status": "degraded", "offline_capable": True},
    {"node_id": "mobile-clinic-unit-3", "region": "field", "status": "offline", "offline_capable": True},
]

SYNC_POLICY = {
    "strategy": "store-and-forward",
    "conflict_resolution": "server-wins-with-manual-review",
    "max_batch_items": 500,
    "retry_schedule": ["1m", "5m", "30m"],
}


class SyncRequest(BaseModel):
    node_id: str = Field(min_length=1, max_length=128)
    payload_items: list[dict] = Field(default_factory=list, max_length=500)


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE_NAME, "version": VERSION}


@app.post("/start", response_model=dict)
async def start(item: dict):
    iid = f"EDGE-COMPUTING-{random.randint(10000, 99999)}"
    result = {
        "id": iid,
        "name": item.get("name", "Untitled"),
        "description": item.get("description", ""),
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    db[iid] = result
    return result


@app.get("/list")
async def list_items() -> list:
    return list(db.values())


@app.get("/list/{item_id}")
async def get_item(item_id: str):
    if item_id not in db:
        raise HTTPException(404, "Not found")
    return db[item_id]


@app.put("/list/{item_id}/update")
async def update_item(item_id: str, data: dict):
    if item_id not in db:
        raise HTTPException(404, "Not found")
    db[item_id].update(data)
    return db[item_id]


@app.delete("/list/{item_id}")
async def delete_item(item_id: str):
    if item_id not in db:
        raise HTTPException(404, "Not found")
    del db[item_id]
    return {"status": "deleted"}


@app.get("/nodes")
async def nodes():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "nodes": EDGE_NODES,
    }


@app.get("/sync/policy")
async def sync_policy():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "policy": SYNC_POLICY,
    }


@app.post("/sync")
async def sync(request: SyncRequest):
    known_ids = {node["node_id"] for node in EDGE_NODES}
    if request.node_id not in known_ids:
        raise HTTPException(404, "Unknown edge node")
    queued = len(request.payload_items)
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "sync_id": str(uuid.uuid4()),
        "node_id": request.node_id,
        "queued_items": queued,
        "status": "queued_for_forwarding",
        "external_actions_attempted": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8026)
