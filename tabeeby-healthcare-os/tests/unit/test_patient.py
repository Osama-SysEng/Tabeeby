import asyncio
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("patient_service_under_test", ROOT / "backend/patient-service/main.py")
patient = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = patient
assert spec.loader is not None
spec.loader.exec_module(patient)


class PatientContractTests(unittest.TestCase):
    def setUp(self):
        patient.PATIENTS_DB.clear()
        patient.AI_PHYSICIANS.clear()
        patient.VITALS_DB.clear()

    def test_patient_registration(self):
        registration = patient.PatientRegistration(name="Test Patient", date_of_birth="1990-01-01", gender="male")
        result = asyncio.run(patient.register_patient(registration))
        self.assertIn("patient_id", result)
        self.assertTrue(result["ai_physician_id"])

    def test_ai_physician_chat(self):
        registration = patient.PatientRegistration(name="Test", date_of_birth="1990-01-01", gender="male")
        result = asyncio.run(patient.register_patient(registration))
        response = asyncio.run(patient.chat_with_ai_physician(result["patient_id"], "I have a headache"))
        self.assertIn("ai_response", response)


if __name__ == "__main__":
    unittest.main()
