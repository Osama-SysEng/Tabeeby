"""Tabeeby Ultra IQ Integration Service - cognitive engine bridge drafts (simulation only)."""
from datetime import datetime, timezone
import random
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tabeeby Ultra IQ Integration Service", version="1.0.0")

SERVICE_NAME = "ultra-iq-integration"
VERSION = "1.0.0"
DISCLAIMER = (
    "Simulation-only mock responses for development and testing. "
    "No live inference is performed. Outputs require human review."
)

db: dict = {}

ENGINE_CAPABILITIES = [
    {"engine": "clinical-summarizer", "label": "Visit note summarization drafts"},
    {"engine": "guideline-matcher", "label": "Guideline reference matching drafts"},
    {"engine": "risk-outline", "label": "Risk factor outline drafts"},
]


class ReasonRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    context: str = Field(default="", max_length=2000)


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE_NAME, "version": VERSION}


@app.post("/start", response_model=dict)
async def start(item: dict):
    iid = f"ULTRA-IQ-INTEGRATION-{random.randint(10000, 99999)}"
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


@app.get("/capabilities")
async def capabilities():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "live_inference": False,
        "disclaimer": DISCLAIMER,
        "capabilities": ENGINE_CAPABILITIES,
    }


@app.get("/bridge/status")
async def bridge_status():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "bridge": "mock",
        "live_inference": False,
        "connected_engines": [cap["engine"] for cap in ENGINE_CAPABILITIES],
    }


@app.post("/reason")
async def reason(request: ReasonRequest):
    query_words = len(request.query.split())
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "live_inference": False,
        "disclaimer": DISCLAIMER,
        "reasoning_id": str(uuid.uuid4()),
        "query_word_count": query_words,
        "outline_draft": [
            "restate-question",
            "list-relevant-context-points",
            "draft-answer-structure",
            "flag-items-needing-human-review",
        ],
        "answer": None,
        "human_review_required": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8009)
