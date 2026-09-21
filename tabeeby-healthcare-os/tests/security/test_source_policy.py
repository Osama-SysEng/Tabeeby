import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from shared.security.source_policy import ApprovedSource, validate_source_response, validate_source_url


class SourcePolicyTests(unittest.TestCase):
    def setUp(self):
        self.source = ApprovedSource("university-1", "fhir.example.edu", "Example Medical University")

    def test_only_exact_https_allowlisted_host_is_accepted(self):
        self.assertEqual(validate_source_url("https://fhir.example.edu/metadata", self.source), "https://fhir.example.edu/metadata")
        with self.assertRaises(ValueError):
            validate_source_url("http://fhir.example.edu/metadata", self.source)
        with self.assertRaises(PermissionError):
            validate_source_url("https://evil.example/metadata", self.source)

    def test_content_type_and_size_are_bounded(self):
        validate_source_response("application/fhir+json; charset=utf-8", 100, self.source)
        with self.assertRaises(ValueError):
            validate_source_response("application/octet-stream", 100, self.source)
        with self.assertRaises(ValueError):
            validate_source_response("application/json", self.source.max_bytes + 1, self.source)


if __name__ == "__main__":
    unittest.main()
