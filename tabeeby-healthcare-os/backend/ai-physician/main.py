"""Tabeeby AI Physician Service - personal AI doctor guidance (simulation-only mocks)."""
from datetime import datetime, timezone
import random
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tabeeby AI Physician Service", version="1.0.0")

SERVICE_NAME = "ai-physician"
VERSION = "1.0.0"
DISCLAIMER = (
    "Simulation-only mock data for development and testing. "
    "Not a medical device. Requires review by a licensed clinician."
)

db: dict = {}


class ConsultRequest(BaseModel):
    patient_id: str = Field(min_length=1, max_length=128)
    symptoms: list[str] = Field(default_factory=list, max_length=20)
    language: str = Field(default="en", max_length=8)


SUPPORTED_LANGUAGES = ["ar", "en", "fr"]

CAPABILITIES = [
    {"id": "triage-guidance", "label": "Symptom triage guidance drafts"},
    {"id": "counseling-support", "label": "General wellness counseling support"},
    {"id": "memory-timeline", "label": "Visit timeline summaries"},
]


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE_NAME, "version": VERSION}


@app.post("/start", response_model=dict)
async def start(item: dict):
    iid = f"AI-PHYSICIAN-{random.randint(10000, 99999)}"
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
        "disclaimer": DISCLAIMER,
        "capabilities": CAPABILITIES,
    }


@app.get("/languages")
async def languages():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "languages": SUPPORTED_LANGUAGES,
    }


@app.post("/consult")
async def consult(request: ConsultRequest):
    symptom_count = len(request.symptoms)
    if symptom_count > 3:
        urgency_draft = "consider-urgent-care-review"
    elif symptom_count > 0:
        urgency_draft = "routine-follow-up"
    else:
        urgency_draft = "no-symptoms-provided"
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "patient_id": request.patient_id,
        "language": request.language if request.language in SUPPORTED_LANGUAGES else "en",
        "symptom_count": symptom_count,
        "urgency_draft": urgency_draft,
        "next_steps": [
            "record-reported-symptoms",
            "prepare-clinician-review-draft",
            "share-self-care-information-draft",
        ],
        "diagnosis": None,
        "human_review_required": True,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8021)
