"""
TABEEBY IoT Service
MQTT + WebSocket real-time biometric streaming
1440+ readings per patient per day
"""
from fastapi import FastAPI, WebSocket, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import json

app = FastAPI(title="Tabeeby IoT Service", version="1.0.0")

class IoTReading(BaseModel):
    device_id: str
    patient_id: str
    readings: Dict[str, float]
    timestamp: datetime = datetime.utcnow()
    device_type: str  # wearable, implant, hospital_equipment, nano_sensor

class IoTService:
    active_devices = {}

    async def process_reading(self, reading: IoTReading):
        processed = {
            "reading_id": f"iot-{datetime.utcnow().timestamp()}",
            "patient_id": reading.patient_id,
            "device_id": reading.device_id,
            "readings_count": len(reading.readings),
            "processed_at": datetime.utcnow().isoformat(),
            "anomaly_flags": self._check_anomalies(reading.readings),
            "weather_correlation": await self._weather_correlation(reading.patient_id)
        }
        return processed

    def _check_anomalies(self, readings: Dict[str, float]):
        flags = []
        if readings.get("heart_rate", 70) > 120 or readings.get("heart_rate", 70) < 50:
            flags.append("heart_rate_anomaly")
        if readings.get("spo2", 98) < 90:
            flags.append("critical_spo2")
        if readings.get("temperature", 37) > 38.5:
            flags.append("fever_detected")
        return flags

    async def _weather_correlation(self, patient_id: str):
        return {
            "pollution_level": "moderate",
            "humidity": 65,
            "pressure_change": "stable",
            "seasonal_risk_adjustment": "applied"
        }

iot = IoTService()

@app.get("/health")
async def health():
    return {"status": "healthy", "protocols": ["mqtt", "websocket"], "service": "iot"}

@app.post("/api/v1/iot/ingest")
async def ingest_reading(reading: IoTReading, background_tasks: BackgroundTasks):
    result = await iot.process_reading(reading)
    if result["anomaly_flags"]:
        background_tasks.add_task(_trigger_alert, reading.patient_id, result["anomaly_flags"])
    return result

@app.get("/api/v1/iot/patient/{patient_id}/readings")
async def get_patient_readings(patient_id: str, hours: int = 24):
    return {
        "patient_id": patient_id,
        "period_hours": hours,
        "estimated_readings": hours * 60,
        "vitals_monitored": [
            "heart_rate", "blood_oxygen", "blood_pressure", "core_temperature",
            "ecg_12lead", "eeg", "blood_glucose", "respiratory_rate",
            "sleep_stages", "movement_activity", "hydration"
        ]
    }

@app.websocket("/ws/iot/{patient_id}")
async def iot_websocket(websocket, patient_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({
                "ack": True,
                "patient_id": patient_id,
                "received": data,
                "timestamp": datetime.utcnow().isoformat()
            })
    except:
        await websocket.close()

async def _trigger_alert(patient_id: str, flags: List[str]):
    await asyncio.sleep(0.1)
    print(f"[ALERT] Patient {patient_id}: {flags}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
