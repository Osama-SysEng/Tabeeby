import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from shared.security.defensive_simulator import SimulationRequest, plan_simulation
from shared.security.file_safety import inspect_upload, inspect_zip_container


class FileAndSimulationTests(unittest.TestCase):
    def test_upload_requires_allowlisted_signature(self):
        verdict = inspect_upload("scan.png", b"not-a-png", declared_content_type="image/png")
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "signature_mismatch")

    def test_upload_rejects_executable_extensions(self):
        verdict = inspect_upload("payload.py", b"print('x')")
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "extension_not_allowed")

    def test_zip_path_traversal_is_rejected(self):
        import io
        import zipfile
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("../../escape.txt", "blocked")
        verdict = inspect_zip_container(stream.getvalue())
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "archive_path_traversal")

    def test_simulator_requires_owner_approval_and_never_exploits(self):
        with self.assertRaises(PermissionError):
            plan_simulation(SimulationRequest("http://127.0.0.1:8000", owner_approval=False))
        result = plan_simulation(SimulationRequest("http://127.0.0.1:8000", owner_approval=True))
        self.assertEqual(result["status"], "planned_only")
        self.assertFalse(result["exploit_payloads_sent"])
        self.assertEqual(result["network_actions_attempted"], [])


if __name__ == "__main__":
    unittest.main()
