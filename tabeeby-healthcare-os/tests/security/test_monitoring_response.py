import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from shared.security.detection import DetectionEngine
from shared.security.incident_response import Incident
from shared.security.monitoring import make_security_event


class MonitoringResponseTests(unittest.TestCase):
    def test_security_event_redacts_sensitive_details(self):
        event = make_security_event("auth.failure", "denied", details={"password": "secret", "nested": {"token": "hidden"}})
        payload = event.to_json()
        self.assertNotIn("secret", payload)
        self.assertNotIn("hidden", payload)
        self.assertIn("REDACTED", payload)

    def test_detection_alerts_on_repeated_failures(self):
        engine = DetectionEngine(window_seconds=60, failed_login_threshold=3)
        self.assertEqual(engine.observe("auth.failure", "ip:203.0.113.10", now=1), [])
        self.assertEqual(engine.observe("auth.failure", "ip:203.0.113.10", now=2), [])
        alerts = engine.observe("auth.failure", "ip:203.0.113.10", now=3)
        self.assertEqual(alerts[0].rule_id, "AUTH-BRUTE-001")

    def test_incident_transitions_are_ordered(self):
        incident = Incident("inc-1", "high")
        incident.transition("triaged", actor="analyst", reason="correlated telemetry")
        incident.transition("contained", actor="analyst", reason="isolate connector")
        with self.assertRaises(ValueError):
            incident.transition("closed", actor="analyst", reason="skip recovery")
        self.assertEqual(incident.propose_containment(target="connector-1"), "isolate:connector-1")


if __name__ == "__main__":
    unittest.main()
