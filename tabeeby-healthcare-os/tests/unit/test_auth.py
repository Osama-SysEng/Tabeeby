import importlib.util
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("TABEEBY_ENV", "test")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-change-me")

spec = importlib.util.spec_from_file_location("auth_service_under_test", ROOT / "backend/auth-service/main.py")
auth = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = auth
assert spec.loader is not None
spec.loader.exec_module(auth)


class AuthContractTests(unittest.TestCase):
    def test_health_contract(self):
        import asyncio
        result = asyncio.run(auth.health())
        self.assertEqual(result["status"], "healthy")

    def test_permission_matrix(self):
        self.assertTrue(auth.PermissionMatrix.check_permission(auth.UserTier.ADMIN, "anything"))
        self.assertFalse(auth.PermissionMatrix.check_permission(auth.UserTier.PATIENT, "admin:read"))


if __name__ == "__main__":
    unittest.main()
