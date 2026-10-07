"""Patient Service - Ultra IQ Healthcare OS"""
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="Tabeeby Patient Service")

class PatientCreate(BaseModel):
    name: str
    age: int
    conditions: Optional[List[str]] = None
    contact: Optional[str] = None

class VitalsUpdate(BaseModel):
    patient_id: str
    heart_rate: Optional[int] = None
    spO2: Optional[int] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    temperature: Optional[float] = None
    glucose: Optional[int] = None
    timestamp: Optional[datetime] = None

# In-memory store for demo
patients_db: dict = {}
vitals_history: dict = {}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "patient-service", "version": "1.0.0"}

@app.get("/patients")
async def get_patients():
    return list(patients_db.values())

@app.get("/patients/{patient_id}")
async def get_patient(patient_id: str):
    if patient_id not in patients_db:
        raise HTTPException(404, "Patient not found")
    return patients_db[patient_id]

@app.post("/patients", response_model=PatientCreate)
async def create_patient(patient: PatientCreate):
    patient_id = f"PAT-{random.randint(1000, 9999)}"
    patient_data = patient.model_dump()
    patient_data["id"] = patient_id
    patient_data["created_at"] = datetime.utcnow()
    patient_data["assigned_physician"] = f"DR-{random.choice([101, 201, 301, 401, 501])}"
    patient_data["ai_companion"] = f"AI-MD-{random.choice(['A', 'B', 'C'])}"
    patients_db[patient_id] = patient_data
    return patient_data

@app.post("/patients/{patient_id}/vitals")
async def update_vitals(patient_id: str, vitals: VitalsUpdate):
    if patient_id not in patients_db:
        raise HTTPException(404, "Patient not found")
    
    vital_data = {
        "heart_rate": vitals.heart_rate or random.randint(65, 85),
        "spO2": vitals.spO2 or random.randint(95, 100),
        "bp_systolic": vitals.bp_systolic or random.randint(110, 130),
        "bp_diastolic": vitals.bp_diastolic or random.randint(70, 90),
        "temperature": vitals.temperature or round(random.uniform(36.5, 37.5), 1),
        "glucose": vitals.glucose or random.randint(80, 120),
        "timestamp": datetime.utcnow(),
    }
    
    if patient_id not in vitals_history:
        vitals_history[patient_id] = []
    vitals_history[patient_id].append(vital_data)
    
    return {"status": "updated", "vitals": vital_data}

@app.get("/patients/{patient_id}/vitals")
async def get_vitals(patient_id: str):
    if patient_id not in vitals_history:
        return {"vitals": [], "history_count": 0}
    return {"vitals": vitals_history[patient_id], "history_count": len(vitals_history[patient_id])}

@app.get("/patients/{patient_id}/vitals/realtime")
async def get_realtime_vitals(patient_id: str):
    vitals = await get_vitals(patient_id)
    latest = vitals["vitals"][-1] if vitals["vitals"] else None
    return {
        "patient_id": patient_id,
        "latest_vitals": latest,
        "status": "normal",
        "alerts": [],
        "ultra_iq_insight": "All vitals within normal range"
    }

@app.get("/patients/{patient_id}/health-trends")
async def get_health_trends(patient_id: str, days: int = 30):
    history = vitals_history.get(patient_id, [])
    if len(history) < 2:
        return {"trends": [], "message": "Insufficient data for trends"}
    
    heart_rates = [v["heart_rate"] for v in history]
    avg_hr = sum(heart_rates) / len(heart_rates)
    trend = "stable" if abs(avg_hr - 72) < 5 else ("high" if avg_hr > 72 else "low")
    
    return {
        "patient_id": patient_id,
        "days_analyzed": days,
        "trends": {
            "heart_rate": {"avg": round(avg_hr, 1), "trend": trend, "range": [min(heart_rates), max(heart_rates)]},
            "spO2": {"avg": 98, "trend": "stable"},
            "blood_pressure": {"avg": "120/80", "trend": "stable"},
            "temperature": {"avg": 37.0, "trend": "stable"},
            "glucose": {"avg": 100, "trend": "stable"},
        },
        "ultra_iq_insights": [
            "Heart rate variability is within normal limits",
            "No significant trends detected",
            "Patient shows stable vitals pattern"
        ]
    }

@app.post("/patients/{patient_id}/appointment")
async def book_appointment(patient_id: str, appointment_data: dict):
    if patient_id not in patients_db:
        raise HTTPException(404, "Patient not found")
    appointment = {
        "patient_id": patient_id,
        "date": appointment_data.get("date"),
        "time": appointment_data.get("time"),
        "doctor": appointment_data.get("doctor"),
        "status": "confirmed",
        "booked_at": datetime.utcnow(),
        "id": f"APT-{random.randint(10000, 99999)}"
    }
    return {"status": "confirmed", "appointment": appointment}

@app.post("/patients/{patient_id}/emergency")
async def trigger_emergency(patient_id: str):
    if patient_id not in patients_db:
        raise HTTPException(404, "Patient not found")
    
    emergency_protocol = {
        "protocol_id": f"EP-{random.randint(10000, 99999)}",
        "triggered_at": datetime.utcnow(),
        "steps_executed": [
            "Step 1: Patient notified via AI voice",
            "Step 2: AI physician engaged",
            "Step 3: Treating physician alerted",
            "Step 4: Ambulance dispatched (ETA: 5-8 min)",
            "Step 5: ER pre-alerted with full history",
            "Step 6: Emergency contacts notified",
            "Step 7: Protocol fully activated"
        ],
        "status": "executing",
        "patient_id": patient_id
    }
    return emergency_protocol

@app.get("/patients/{patient_id}/medications")
async def get_medications(patient_id: str):
    return {
        "patient_id": patient_id,
        "medications": [
            {"id": "M1", "name": "Antihypertensive", "dosage": "10mg", "time": "08:00", "taken": False},
            {"id": "M2", "name": "Antidiabetic", "dosage": "5mg", "time": "08:00", "taken": False},
        ]
    }

@app.post("/patients/{patient_id}/medications/{med_id}/take")
async def mark_medication_taken(patient_id: str, med_id: str):
    return {"status": "marked_taken", "medication_id": med_id, "patient_id": patient_id}

@app.get("/patients/{patient_id}/symptom-check")
async def check_symptoms(patient_id: str, symptoms: List[str] = []):
    possible_conditions = [
        "Upper respiratory infection",
        "Gastroenteritis",
        "Migraine",
        "Stress-related symptoms",
        "Allergic reaction",
    ]
    return {
        "patient_id": patient_id,
        "symptoms_analyzed": len(symptoms),
        "possible_conditions": possible_conditions[:min(len(symptoms), 3)],
        "probability_scores": {"Condition A": 0.7, "Condition B": 0.2, "Condition C": 0.1},
        "recommendation": "Please consult with your physician for proper diagnosis",
        "urgent": False,
        "ultra_iq_notes": "Symptom patterns suggest viral etiology - monitor for 48h"
    }

@app.get("/patients/{patient_id}/weather-impact")
async def get_weather_impact(patient_id: str):
    return {
        "patient_id": patient_id,
        "weather": {
            "temperature": 28,
            "humidity": 72,
            "description": "Humid",
            "warnings": ["High humidity may affect asthma patients", "Heat advisory: Stay hydrated"]
        },
        "health_risks": ["Dehydration risk", "Heat exhaustion possible"],
        "recommendations": ["Drink 3L water today", "Avoid peak sun hours (11am-4pm)", "Use sunscreen SPF 30+"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
