import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("identity_under_test", ROOT / "backend/auth-service/identity.py")
identity = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = identity
assert spec.loader is not None
spec.loader.exec_module(identity)


class IdentityPrivacyTests(unittest.TestCase):
    def test_email_normalization_is_deterministic(self):
        self.assertEqual(identity.normalize_email("  Doctor@Example.COM "), "doctor@example.com")

    def test_phone_requires_country_code(self):
        self.assertEqual(identity.normalize_phone("+20 (100) 123-4567"), "+201001234567")
        with self.assertRaises(identity.ContactValidationError):
            identity.normalize_phone("01001234567")

    def test_lookup_digest_is_keyed_and_type_scoped(self):
        secret = b"x" * 32
        email = identity.contact_lookup_digest("email", "doctor@example.com", secret)
        phone = identity.contact_lookup_digest("phone", "+201001234567", secret)
        self.assertEqual(len(email), 64)
        self.assertNotEqual(email, phone)
        with self.assertRaises(ValueError):
            identity.contact_lookup_digest("email", "doctor@example.com", b"short")


if __name__ == "__main__":
    unittest.main()
