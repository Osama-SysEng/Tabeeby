"""Privacy-preserving contact identity helpers.

Raw email/phone values must be collected and verified by an approved identity
provider. This module provides deterministic keyed lookup values and avoids
putting contact details into public IDs, URLs, logs, or JWT claims.
"""
from __future__ import annotations

import hashlib
import hmac
import re
import unicodedata


class ContactValidationError(ValueError):
    pass


def normalize_email(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().casefold()
    if len(value) > 320 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        raise ContactValidationError("Invalid email format")
    return value


def normalize_phone(value: str, default_region: str | None = None) -> str:
    del default_region  # Region parsing belongs in a vetted telecom library.
    compact = re.sub(r"[\s().-]+", "", value.strip())
    if not re.fullmatch(r"\+[1-9]\d{7,14}", compact):
        raise ContactValidationError("Phone must be E.164-like and include country code")
    return compact


def contact_lookup_digest(kind: str, normalized_value: str, secret: bytes) -> str:
    if kind not in {"email", "phone"}:
        raise ValueError("kind must be email or phone")
    if len(secret) < 32:
        raise ValueError("lookup secret must be at least 32 bytes")
    return hmac.new(secret, f"{kind}:v1:{normalized_value}".encode(), hashlib.sha256).hexdigest()
