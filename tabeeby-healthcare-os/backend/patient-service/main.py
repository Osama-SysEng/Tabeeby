"""
TABEEBY Patient Service
Lifetime persistent memory, AI Virtual Physician, IoT Integration, Emergency Protocol
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
import asyncio
from enum import Enum

app = FastAPI(title="Tabeeby Patient Service", version="1.0.0")

# Simulated database (in production: PostgreSQL + TimescaleDB + Neo4j + Qdrant)
PATIENTS_DB = {}
VITALS_DB = {}
AI_PHYSICIANS = {}
EMERGENCY_LOGS = []

class AlertLevel(str, Enum):
    LEVEL_1 = "level_1"  # Patient notification
    LEVEL_2 = "level_2"  # Virtual physician intervention
    LEVEL_3 = "level_3"  # Assigned physician alert
    LEVEL_4 = "level_4"  # Full emergency protocol

class PatientRegistration(BaseModel):
    name: str
    date_of_birth: str = Field(min_length=10, max_length=10, pattern=r"^\d{4}-\d{2}-\d{2}$")
    gender: str = Field(min_length=1, max_length=32)
    blood_type: Optional[str] = Field(default=None, max_length=8)
    allergies: List[str] = Field(default_factory=list, max_length=100)
    chronic_conditions: List[str] = Field(default_factory=list, max_length=100)
    emergency_contact: Dict[str, str] = Field(default_factory=dict)
    language: str = "auto"
    dialect: Optional[str] = None

class VitalSigns(BaseModel):
    patient_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    heart_rate: Optional[float] = Field(default=None, ge=0, le=300)
    blood_pressure_systolic: Optional[float] = Field(default=None, ge=0, le=400)
    blood_pressure_diastolic: Optional[float] = Field(default=None, ge=0, le=300)
    spo2: Optional[float] = Field(default=None, ge=0, le=100)
    temperature: Optional[float] = Field(default=None, ge=20, le=50)
    ecg_leads: Optional[List[float]] = None
    eeg_data: Optional[List[float]] = None
    blood_glucose: Optional[float] = Field(default=None, ge=0, le=2000)
    respiratory_rate: Optional[float] = Field(default=None, ge=0, le=200)
    sleep_stage: Optional[str] = None
    activity_level: Optional[str] = None
    hydration_index: Optional[float] = Field(default=None, ge=0, le=1)

class AIPhysician:
    """Personal AI Physician assigned permanently at registration"""
    def __init__(self, patient_id: str, language: str = "auto"):
        self.patient_id = patient_id
        self.language = language
        self.dialect = None
        self.memory = []  # Lifetime persistent memory
        self.communication_style = "adaptive"
        self.emotional_patterns = {}
        self.created_at = datetime.utcnow()

    async def learn_dialect(self, sample_text: str):
        """Auto-learn patient's exact dialect on first message"""
        # Simulated dialect detection
        self.dialect = f"detected_dialect_{hash(sample_text) % 1000}"
        self.memory.append({
            "type": "dialect_learned",
            "dialect": self.dialect,
            "timestamp": datetime.utcnow().isoformat()
        })
        return self.dialect

    async def add_memory(self, event: Dict[str, Any]):
        """Never forgets any data point across entire lifetime"""
        self.memory.append({
            **event,
            "timestamp": datetime.utcnow().isoformat(),
            "memory_id": str(uuid.uuid4())
        })

    async def get_context(self, query: str) -> Dict[str, Any]:
        """Retrieve relevant lifetime context for any query"""
        # In production: Vector search through Qdrant
        relevant = [m for m in self.memory if query.lower() in str(m).lower()]
        return {
            "patient_id": self.patient_id,
            "relevant_memories": relevant[-50:],  # Last 50 relevant
            "total_memories": len(self.memory),
            "language": self.language,
            "dialect": self.dialect
        }

    async def generate_response(self, patient_message: str) -> Dict[str, Any]:
        """Generate personalized response in patient's language/dialect"""
        context = await self.get_context(patient_message)

        # Simulated AI physician response
        response = {
            "message": f"[AI Physician in {self.language}/{self.dialect}] I understand your concern about '{patient_message}'. Based on your history...",
            "recommendations": [
                "Monitor symptoms for 24 hours",
                "Stay hydrated",
                "Contact physician if condition worsens"
            ],
            "confidence": 0.95,
            "context_used": len(context["relevant_memories"])
        }

        await self.add_memory({
            "type": "conversation",
            "patient_message": patient_message,
            "ai_response": response["message"]
        })

        return response

@app.get("/health")
async def health():
    return {"status": "healthy", "patients": len(PATIENTS_DB), "service": "patient"}

@app.post("/api/v1/patients/register")
async def register_patient(registration: PatientRegistration):
    """Register patient + assign permanent AI physician"""
    patient_id = str(uuid.uuid4())

    patient = {
        "id": patient_id,
        **registration.dict(),
        "registered_at": datetime.utcnow().isoformat(),
        "ai_physician_assigned": True,
        "lifetime_memory_active": True
    }

    PATIENTS_DB[patient_id] = patient

    # Assign permanent AI physician
    ai_physician = AIPhysician(patient_id, registration.language)
    AI_PHYSICIANS[patient_id] = ai_physician

    # Auto-detect dialect if language is auto
    if registration.language == "auto":
        await ai_physician.learn_dialect(f"Sample from {registration.name}")

    return {
        "patient_id": patient_id,
        "ai_physician_id": f"ai-physician-{patient_id}",
        "language_detected": ai_physician.language,
        "dialect": ai_physician.dialect,
        "message": "Patient registered with lifetime AI physician assignment"
    }

@app.get("/api/v1/patients/{patient_id}")
async def get_patient(patient_id: str):
    """Get complete patient profile with lifetime history"""
    if patient_id not in PATIENTS_DB:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_DB[patient_id]
    ai_physician = AI_PHYSICIANS.get(patient_id)

    return {
        **patient,
        "ai_physician": {
            "language": ai_physician.language if ai_physician else None,
            "dialect": ai_physician.dialect if ai_physician else None,
            "total_memories": len(ai_physician.memory) if ai_physician else 0,
            "created_at": ai_physician.created_at.isoformat() if ai_physician else None
        },
        "vitals_summary": VITALS_DB.get(patient_id, {})
    }

@app.post("/api/v1/patients/{patient_id}/vitals")
async def record_vitals(patient_id: str, vitals: VitalSigns, background_tasks: BackgroundTasks):
    """Record IoT vitals with anomaly detection"""
    if patient_id not in PATIENTS_DB:
        raise HTTPException(status_code=404, detail="Patient not found")
    if vitals.patient_id != patient_id:
        raise HTTPException(status_code=422, detail="vitals.patient_id must match the path patient_id")

    if patient_id not in VITALS_DB:
        VITALS_DB[patient_id] = []

    VITALS_DB[patient_id].append(vitals.dict())

    # Background: Anomaly detection
    background_tasks.add_task(_anomaly_detection, patient_id, vitals)

    return {"status": "recorded", "timestamp": vitals.timestamp.isoformat()}

@app.get("/api/v1/patients/{patient_id}/vitals/history")
async def get_vitals_history(patient_id: str, hours: int = 24):
    """Get vital signs history"""
    if patient_id not in VITALS_DB:
        return {"vitals": [], "count": 0}

    cutoff = datetime.utcnow() - timedelta(hours=hours)
    vitals = [v for v in VITALS_DB[patient_id] if v["timestamp"] > cutoff]

    return {
        "vitals": vitals,
        "count": len(vitals),
        "readings_per_day": len(vitals) / (hours / 24) if hours > 0 else 0
    }

@app.post("/api/v1/patients/{patient_id}/ai-physician/chat")
async def chat_with_ai_physician(patient_id: str, message: str):
    """Chat with personal AI physician"""
    if patient_id not in AI_PHYSICIANS:
        raise HTTPException(status_code=404, detail="AI physician not found")

    ai_physician = AI_PHYSICIANS[patient_id]
    response = await ai_physician.generate_response(message)

    return {
        "patient_id": patient_id,
        "ai_response": response,
        "language": ai_physician.language,
        "dialect": ai_physician.dialect
    }

@app.get("/api/v1/patients/{patient_id}/ai-physician/memory")
async def get_ai_memory(patient_id: str, query: Optional[str] = None):
    """Retrieve AI physician lifetime memory"""
    if patient_id not in AI_PHYSICIANS:
        raise HTTPException(status_code=404, detail="AI physician not found")

    ai_physician = AI_PHYSICIANS[patient_id]

    if query:
        context = await ai_physician.get_context(query)
        return context

    return {
        "total_memories": len(ai_physician.memory),
        "memories": ai_physician.memory[-100:],  # Last 100
        "language": ai_physician.language,
        "dialect": ai_physician.dialect
    }

@app.post("/api/v1/patients/{patient_id}/emergency/trigger")
async def trigger_emergency(patient_id: str, alert_level: AlertLevel = AlertLevel.LEVEL_4):
    """7-step autonomous emergency protocol"""
    if patient_id not in PATIENTS_DB:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_DB[patient_id]
    emergency_id = str(uuid.uuid4())

    # Step 1: Critical threshold detected (already detected by IoT)
    # Step 2: Patient device alert
    # Step 3: Virtual physician real-time guidance
    # Step 4: Assigned physician alert
    # Step 5: Nearest ambulance GPS dispatch
    # Step 6: Nearest ER pre-alert
    # Step 7: Emergency contact notification

    emergency_log = {
        "emergency_id": emergency_id,
        "patient_id": patient_id,
        "alert_level": alert_level.value,
        "steps_executed": [
            "Critical threshold detected by IoT sensor",
            "Patient device: Emergency alert + AI voice stabilization",
            "Virtual physician: Real-time clinical guidance activated",
            "Assigned physician: Push notification + full vitals summary",
            "Nearest ambulance: Automated GPS dispatch",
            "Nearest ER: Pre-alert with complete medical history",
            "Emergency contact: Immediate notification sent"
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "human_intervention_required": True,
        "mode": "simulation_only",
        "external_actions_attempted": []
    }

    EMERGENCY_LOGS.append(emergency_log)

    return {
        "emergency_id": emergency_id,
        "status": "simulation_only",
        "mode": "non_actuating",
        "steps": 7,
        "external_actions_attempted": [],
        "human_intervention_required": True,
        "approval_required_before_external_delivery": True,
        "message": "Emergency response prepared for review; no external service was contacted"
    }

@app.get("/api/v1/patients/{patient_id}/disease-lifecycle")
async def disease_lifecycle(patient_id: str):
    """Full disease lifecycle management overview"""
    if patient_id not in PATIENTS_DB:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "patient_id": patient_id,
        "lifecycle_stages": [
            {"stage": "symptom_onset", "status": "monitored", "ai_action": "Differential diagnosis support"},
            {"stage": "diagnosis", "status": "pending", "ai_action": "Personalized treatment protocol"},
            {"stage": "treatment", "status": "pending", "ai_action": "Real-time monitoring + adjustment"},
            {"stage": "recovery", "status": "pending", "ai_action": "Progress tracking + milestone validation"},
            {"stage": "chronic_management", "status": "pending", "ai_action": "Long-term management optimization"},
            {"stage": "preventive", "status": "active", "ai_action": "Risk factor identification + intervention"},
            {"stage": "lifetime_optimization", "status": "continuous", "ai_action": "Health trajectory improvement"}
        ],
        "ai_physician_continuous_actions": [
            "Updated disease research relevant to patient's case",
            "Emerging treatment options + clinical trial opportunities",
            "Patient-specific anomaly patterns discovered by Ultra IQ",
            "Predictive alerts — deterioration predicted before symptoms"
        ]
    }

async def _anomaly_detection(patient_id: str, vitals: VitalSigns):
    """Background anomaly detection with graduated alert system"""
    await asyncio.sleep(0.1)

    anomalies = []

    if vitals.heart_rate and (vitals.heart_rate < 50 or vitals.heart_rate > 120):
        anomalies.append({"type": "heart_rate", "value": vitals.heart_rate, "severity": "high"})

    if vitals.spo2 and vitals.spo2 < 90:
        anomalies.append({"type": "spo2", "value": vitals.spo2, "severity": "critical"})

    if vitals.temperature and (vitals.temperature < 35.5 or vitals.temperature > 38.5):
        anomalies.append({"type": "temperature", "value": vitals.temperature, "severity": "medium"})

    if anomalies:
        # Determine alert level
        if any(a["severity"] == "critical" for a in anomalies):
            alert_level = AlertLevel.LEVEL_4
        elif any(a["severity"] == "high" for a in anomalies):
            alert_level = AlertLevel.LEVEL_3
        else:
            alert_level = AlertLevel.LEVEL_2

        print(f"[ANOMALY] Patient {patient_id}: {len(anomalies)} anomalies detected. Alert: {alert_level.value}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
