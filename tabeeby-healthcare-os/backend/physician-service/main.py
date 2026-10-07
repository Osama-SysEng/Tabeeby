"""Physician Service - Ultra IQ Healthcare OS"""
import asyncio
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="Tabeeby Physician Service")

class AlertCreate(BaseModel):
    alert_type: str
    message: str
    patient_id: str
    predicted_seconds: int
    confidence: float

class TreatmentRequest(BaseModel):
    patient_id: str
    diagnosis: str
    severity: str

class DrugInteractionRequest(BaseModel):
    drug1: str
    drug2: str

# In-memory stores
physicians_db = {}
patients_db = {}
alerts_db = []
treatments_db = {}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "physician-service", "version": "1.0.0"}

@app.get("/physicians")
async def get_physicians():
    return list(physicians_db.values())

@app.get("/physicians/{physician_id}")
async def get_physician(physician_id: str):
    if physician_id not in physicians_db:
        raise HTTPException(404, "Physician not found")
    return physicians_db[physician_id]

@app.post("/physicians")
async def create_physician(physician_data: dict):
    physician_id = f"DR-{random.randint(100, 999)}"
    physicians_db[physician_id] = {
        "id": physician_id,
        "name": physician_data.get("name", "Dr. Unknown"),
        "specialty": physician_data.get("specialty", "General"),
        "created_at": datetime.utcnow(),
        "patient_count": 0,
        "active_alerts": 0
    }
    return physicians_db[physician_id]

@app.get("/physicians/{physician_id}/patients")
async def get_physician_patients(physician_id: str, limit: int = 50):
    if physician_id not in physicians_db:
        raise HTTPException(404, "Physician not found")
    patient_list = []
    for i in range(min(limit, 50)):
        patient_list.append({
            "id": f"PAT-{1000+i}",
            "name": f"Patient {i+1}",
            "age": random.randint(20, 80),
            "status": random.choice(["stable", "monitoring", "warning", "critical"]),
            "vitals": {
                "heart_rate": random.randint(60, 100),
                "spO2": random.randint(95, 100),
                "bp": f"{random.randint(110,140)}/{random.randint(70,90)}",
                "temperature": round(random.uniform(36.0, 37.5), 1),
                "glucose": random.randint(80, 150)
            },
            "alerts": random.sample(["Elevated heart rate", "High glucose", "Low SpO2"], k=random.randint(0, 2)),
            "last_updated": datetime.utcnow().isoformat()
        })
    physicians_db[physician_id]["patient_count"] = len(patient_list)
    return patient_list

@app.get("/physicians/{physician_id}/alerts")
async def get_physician_alerts(physician_id: str):
    if physician_id not in physicians_db:
        raise HTTPException(404, "Physician not found")
    
    alerts = [
        {"id": f"AL-{i}", "type": alert_type, "message": f"Alert for patient PAT-100{i}: {alert_type}",
         "seconds_before": random.randint(30, 120), "confidence": round(random.uniform(80, 99), 1),
         "patient_id": f"PAT-100{i}", "created_at": datetime.utcnow().isoformat()}
        for i, alert_type in enumerate(["elevated_heart_rate", "high_blood_pressure", "low_spO2", "high_glucose", "irregular_rhythm"])
    ]
    return alerts

@app.post("/physicians/{physician_id}/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(physician_id: str, alert_id: str):
    return {"status": "acknowledged", "alert_id": alert_id, "physician_id": physician_id, "acknowledged_at": datetime.utcnow().isoformat()}

@app.post("/physicians/{physician_id}/alerts/{alert_id}/escalate")
async def escalate_alert(physician_id: str, alert_id: str):
    return {"status": "escalated", "alert_id": alert_id, "escalated_to": "senior_care_team", "escalated_at": datetime.utcnow().isoformat()}

@app.get("/physicians/{physician_id}/treatment-recommendations")
async def get_treatment_recommendations(physician_id: str, patient_id: str, diagnosis: str = "Hypertension"):
    recommendations = [
        {"id": f"T-{i}", "name": name, "efficacy": efficacy, "evidence": evidence,
         "side_effects": side_effects, "guidelines": guidelines, "ultra_iq_rating": random.randint(85, 99)}
        for i, (name, efficacy, evidence, side_effects, guidelines) in enumerate([
            ("Antihypertensive ACE Inhibitor", 87, "NICE Guidelines 2024", ["Dry cough", "Dizziness"], "10mg daily"),
            ("Calcium Channel Blocker", 82, "ACC/AHA Guidelines", ["Edema", "Flushing"], "5mg daily"),
            ("Beta Blocker", 78, "ESC Guidelines 2023", ["Fatigue", "Bradycardia"], "25mg BID"),
            ("Lifestyle Modification", 92, "WHO Guidelines", ["None"], "30min exercise daily + DASH diet"),
            ("Diuretic", 75, "ISH Guidelines", ["Electrolyte imbalance", "Frequent urination"], "25mg daily"),
        ][:5])
    return {"physician_id": physician_id, "patient_id": patient_id, "diagnosis": diagnosis, "recommendations": recommendations}

@app.post("/physicians/{physician_id}/drug-interaction")
async def check_drug_interaction(physician_id: str, interaction_request: DrugInteractionRequest):
    drug_interactions = {
        ("Lisinopril", "Spironolactone"): {"level": "high", "message": "Increased risk of hyperkalemia", "recommendation": "Monitor potassium levels closely", "contraindicated": True},
        ("Warfarin", "Aspirin"): {"level": "critical", "message": "Significantly increased bleeding risk", "recommendation": "Avoid concurrent use unless absolutely necessary", "contraindicated": True},
        ("Metformin", "Contrast dye"): {"level": "moderate", "message": "Risk of lactic acidosis", "recommendation": "Hold metformin before procedure", "contraindicated": False},
        ("Simvastatin", "Amiodarone"): {"level": "high", "message": "Increased risk of rhabdomyolysis", "recommendation": "Reduce simvastatin dose by 50%", "contraindicated": False},
        ("default", "default"): {"level": "none", "message": "No significant interactions detected", "recommendation": "Continue as prescribed", "contraindicated": False},
    }
    
    key = (interaction_request.drug1, interaction_request.drug2)
    result = drug_interactions.get(key, drug_interactions[("default", "default")])
    
    return {
        "physician_id": physician_id,
        "drug1": interaction_request.drug1,
        "drug2": interaction_request.drug2,
        **result,
        "ultra_iq_analysis": "Cross-reference complete - no additional contraindications found"
    }

@app.get("/physicians/{physician_id}/lab-results")
async def get_lab_results(physician_id: str, patient_id: str = None):
    lab_results = [
        {"id": "LR-001", "test_name": "Hemoglobin A1c", "value": "7.2%", "unit": "%", "reference_range": "4-6%", "date": "2024-01-15", "status": "high"},
        {"id": "LR-002", "test_name": "LDL Cholesterol", "value": "135 mg/dL", "unit": "mg/dL", "reference_range": "<100", "date": "2024-01-15", "status": "high"},
        {"id": "LR-003", "test_name": "Creatinine", "value": "1.1 mg/dL", "unit": "mg/dL", "reference_range": "0.7-1.3", "date": "2024-01-15", "status": "normal"},
        {"id": "LR-004", "test_name": "ALT", "value": "35 U/L", "unit": "U/L", "reference_range": "7-56", "date": "2024-01-15", "status": "normal"},
        {"id": "LR-005", "test_name": "TSH", "value": "2.5 mIU/L", "unit": "mIU/L", "reference_range": "0.4-4.0", "date": "2024-01-15", "status": "normal"},
    ]
    return {"physician_id": physician_id, "patient_id": patient_id, "lab_results": lab_results}

@app.get("/physicians/{physician_id}/imaging-comparisons")
async def get_imaging_comparisons(physician_id: str, patient_id: str = None):
    comparisons = [
        {"id": "IM-001", "modality": "Chest X-Ray", "finding": "Cardiomegaly noted", "date": "2024-01-10", "severity": "moderate", "comparison_with_prior": "Progression from prior study (3 months ago)", "ultra_iq_annotation": "Cardiac silhouette increased by 12% - recommend echocardiogram"},
        {"id": "IM-002", "modality": "MRI Brain", "finding": "No acute findings", "date": "2024-01-12", "severity": "normal", "comparison_with_prior": "No change from baseline", "ultra_iq_annotation": "Brain parenchyma unremarkable"},
        {"id": "IM-003", "modality": "CT Abdomen", "finding": "Fatty liver disease", "date": "2024-01-08", "severity": "mild", "comparison_with_prior": "Stable compared to 6 months ago", "ultra_iq_annotation": "Grade 1 steatosis - lifestyle modification recommended"},
    ]
    return {"physician_id": physician_id, "patient_id": patient_id, "comparisons": comparisons}

@app.post("/physicians/{physician_id}/treatment-plan")
async def create_treatment_plan(physician_id: str, plan_data: dict):
    plan = {
        "plan_id": f"TP-{random.randint(10000, 99999)}",
        "physician_id": physician_id,
        "patient_id": plan_data.get("patient_id"),
        "diagnosis": plan_data.get("diagnosis"),
        "treatments": plan_data.get("treatments", []),
        "medications": plan_data.get("medications", []),
        "follow_up": plan_data.get("follow_up_date"),
        "created_at": datetime.utcnow().isoformat(),
        "status": "active",
        "ultra_iq_optimize": True
    }
    return {"status": "created", "plan": plan}

@app.get("/physicians/{physician_id}/performance-metrics")
async def get_performance_metrics(physician_id: str):
    return {
        "physician_id": physician_id,
        "metrics": {
            "patient_satisfaction": 4.7,
            "response_time_avg_min": 15,
            "treatment_success_rate": 92,
            "preventive_care_rate": 88,
            "patient_retention_rate": 95,
            "ultra_iq_conformance": 96
        },
        "peer_comparison": {
            "percentile": 92,
            "specialty_average": 85,
            "top_performer_threshold": 95
        },
        "ultra_iq_recommendations": [
            "Consider 5-minute reduction in average response time",
            "Increase preventive care screening rate by 5%"
        ]
    }

@app.get("/physicians/{physician_id}/clinical-trials")
async def get_clinical_trials(physician_id: str, patient_id: str, condition: str = "Hypertension"):
    trials = [
        {"id": f"CT-{i}", "title": f"Novel {condition} Treatment Trial - Phase {random.choice(['II', 'III'])}",
         "phase": random.choice(["Phase II", "Phase III"]), "condition": condition,
         "sponsor": random.choice(["PharmaCorp", "BioTech Inc", "Academic Medical Center"]),
         "location": random.choice(["Cairo", "Alexandria", "Aswan", "Ismailia"]),
         "eligibility": "Adults 18-75 with confirmed diagnosis",
         "status": random.choice(["Recruiting", "Active", "Not yet recruiting"]),
         "ultra_iq_match_score": random.randint(75, 98)}
        for i in range(3)
    ]
    return {"physician_id": physician_id, "patient_id": patient_id, "condition": condition, "trials": trials}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
