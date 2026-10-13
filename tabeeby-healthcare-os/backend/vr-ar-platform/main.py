"""Tabeeby VR/AR Platform Service - training session planning drafts (simulation only)."""
from datetime import datetime, timezone
import random
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tabeeby VR/AR Platform Service", version="1.0.0")

SERVICE_NAME = "vr-ar-platform"
VERSION = "1.0.0"
DISCLAIMER = (
    "Simulation-only training content for education and testing. "
    "No clinical guidance is provided. Requires instructor review."
)

db: dict = {}

SCENARIOS = [
    {"scenario_id": "trauma-triage-vr", "label": "Emergency triage rehearsal", "modality": "vr"},
    {"scenario_id": "anatomy-overlay-ar", "label": "Anatomy overlay study aid", "modality": "ar"},
    {"scenario_id": "or-teamwork-vr", "label": "Operating room teamwork drill", "modality": "vr"},
]

DEVICES = [
    {"device_id": "headset-vr-01", "kind": "vr-headset", "status": "available"},
    {"device_id": "glasses-ar-02", "kind": "ar-glasses", "status": "available"},
    {"device_id": "haptic-glove-03", "kind": "haptic-gloves", "status": "maintenance"},
]


class SessionPlanRequest(BaseModel):
    scenario_id: str = Field(min_length=1, max_length=128)
    trainee_id: str = Field(min_length=1, max_length=128)


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE_NAME, "version": VERSION}


@app.post("/start", response_model=dict)
async def start(item: dict):
    iid = f"VR-AR-PLATFORM-{random.randint(10000, 99999)}"
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


@app.get("/scenarios")
async def scenarios():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "scenarios": SCENARIOS,
    }


@app.get("/devices")
async def devices():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "devices": DEVICES,
    }


@app.post("/sessions/plan")
async def plan_session(request: SessionPlanRequest):
    known_scenarios = {scenario["scenario_id"] for scenario in SCENARIOS}
    if request.scenario_id not in known_scenarios:
        raise HTTPException(404, "Unknown scenario")
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "session_id": str(uuid.uuid4()),
        "scenario_id": request.scenario_id,
        "trainee_id": request.trainee_id,
        "agenda_draft": [
            "briefing",
            "guided-rehearsal",
            "free-practice",
            "assessment-draft",
            "debrief",
        ],
        "external_actions_attempted": [],
        "instructor_review_required": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8025)
