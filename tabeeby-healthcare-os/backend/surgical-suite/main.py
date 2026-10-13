"""Tabeeby Surgical Suite Service - non-actuating surgery planning drafts (simulation only)."""
from datetime import datetime, timezone
import random
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tabeeby Surgical Suite Service", version="1.0.0")

SERVICE_NAME = "surgical-suite"
VERSION = "1.0.0"
DISCLAIMER = (
    "Simulation-only planning drafts for training and testing. "
    "Live actuation is disabled. No device is controlled. "
    "Requires review by qualified surgical staff."
)

db: dict = {}

PROCEDURES = [
    {"procedure_id": "lap-chole-sim", "label": "Laparoscopic cholecystectomy rehearsal", "modality": "vr-simulation"},
    {"procedure_id": "cataract-sim", "label": "Cataract procedure rehearsal", "modality": "ar-guidance-draft"},
    {"procedure_id": "ortho-drill-sim", "label": "Orthopedic drilling rehearsal", "modality": "robotic-path-draft"},
]

SAFETY_INTERLOCKS = [
    {"interlock": "live_actuation_disabled", "state": "enforced"},
    {"interlock": "dual-surgeon-approval-required", "state": "enforced"},
    {"interlock": "device-link", "state": "disconnected-simulation-only"},
]


class SimulateRequest(BaseModel):
    procedure_id: str = Field(min_length=1, max_length=128)
    surgeon_id: str = Field(min_length=1, max_length=128)


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE_NAME, "version": VERSION}


@app.post("/start", response_model=dict)
async def start(item: dict):
    iid = f"SURGICAL-SUITE-{random.randint(10000, 99999)}"
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


@app.get("/procedures")
async def procedures():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "disclaimer": DISCLAIMER,
        "procedures": PROCEDURES,
    }


@app.get("/safety-interlocks")
async def safety_interlocks():
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "mode": "non_actuating",
        "interlocks": SAFETY_INTERLOCKS,
    }


@app.post("/simulate")
async def simulate(request: SimulateRequest):
    known_ids = {proc["procedure_id"] for proc in PROCEDURES}
    if request.procedure_id not in known_ids:
        raise HTTPException(404, "Unknown procedure")
    return {
        "service": SERVICE_NAME,
        "simulation_only": True,
        "mode": "non_actuating",
        "disclaimer": DISCLAIMER,
        "simulation_id": str(uuid.uuid4()),
        "procedure_id": request.procedure_id,
        "surgeon_id": request.surgeon_id,
        "plan_draft": [
            "verify-patient-identity",
            "review-imaging-draft",
            "rehearse-approach-path",
            "prepare-instrument-checklist-draft",
            "debrief-and-log-draft",
        ],
        "external_actions_attempted": [],
        "human_intervention_required": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8008)
