"""Executable safety checks for the simulation-first prototype."""
import asyncio
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SafetyBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emergency = load_module("safety_emergency", ROOT / "backend/emergency-service/main.py")
        cls.nano = load_module("safety_nano", ROOT / "backend/nano-os/main.py")
        cls.patient = load_module("safety_patient", ROOT / "backend/patient-service/main.py")

    def test_emergency_is_non_actuating(self):
        trigger = self.emergency.EmergencyTrigger(patient_id="p-1", triggered_by="test", vitals_snapshot={})
        result = asyncio.run(self.emergency.emergency.simulate_protocol(trigger))
        self.assertEqual(result["status"], "simulation_only")
        self.assertEqual(result["external_actions_attempted"], [])
        self.assertTrue(result["human_intervention_required"])

    def test_nano_execution_is_rejected(self):
        with self.assertRaises(Exception) as raised:
            asyncio.run(self.nano.execute_nano_surgery("plan-1"))
        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(raised.exception.detail["code"], "LIVE_ACTUATION_DISABLED")

    def test_invalid_patient_input_is_rejected(self):
        with self.assertRaises(Exception):
            self.patient.PatientRegistration(name="Test", date_of_birth="not-a-date", gender="patient")

    def test_vitals_patient_identity_must_match_path(self):
        vitals = self.patient.VitalSigns(patient_id="different", spo2=98)
        self.patient.PATIENTS_DB["p-1"] = {"id": "p-1"}
        with self.assertRaises(Exception) as raised:
            asyncio.run(self.patient.record_vitals("p-1", vitals, type("Tasks", (), {"add_task": lambda *args: None})()))
        self.assertEqual(raised.exception.status_code, 422)


if __name__ == "__main__":
    unittest.main()
