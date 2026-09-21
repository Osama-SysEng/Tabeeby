import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from shared.security.ip_policy import reject_public_endpoint_target, resolve_client_ip
from shared.security.python_policy import inspect_python_source
from shared.security.service_keys import sign_request, verify_request


class SecurityControlTests(unittest.TestCase):
    def test_python_policy_rejects_dynamic_execution_and_network_imports(self):
        findings = inspect_python_source("import os\nexec(user_code)\n")
        rules = {finding.rule for finding in findings}
        self.assertIn("blocked_import", rules)
        self.assertIn("blocked_call", rules)

    def test_python_policy_enforces_size_limit(self):
        self.assertEqual(inspect_python_source("x = 1", max_bytes=2)[0].rule, "size_limit")

    def test_untrusted_peer_cannot_spoof_forwarded_ip(self):
        self.assertEqual(resolve_client_ip("203.0.113.10", "10.0.0.8", ["10.0.0.0/8"]), "203.0.113.10")
        self.assertEqual(resolve_client_ip("10.0.0.8", "198.51.100.7, 10.0.0.9", ["10.0.0.0/8"]), "198.51.100.7")

    def test_ssrf_prone_local_targets_are_rejected(self):
        with self.assertRaises(ValueError):
            reject_public_endpoint_target("127.0.0.1")

    def test_service_signature_requires_fresh_timestamp(self):
        secret = b"s" * 32
        signed = sign_request("auth", secret, "POST", "/internal/patient", b"{}", timestamp=1000, nonce="n-1")
        self.assertTrue(verify_request(signed, secret, "POST", "/internal/patient", b"{}", now=1040))
        self.assertFalse(verify_request(signed, secret, "POST", "/internal/patient", b"{}", now=1100))
        self.assertFalse(verify_request(signed, secret, "POST", "/internal/patient", b"{\"tampered\":true}", now=1040))


if __name__ == "__main__":
    unittest.main()
