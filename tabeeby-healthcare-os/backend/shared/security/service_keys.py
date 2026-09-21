"""HMAC service-to-service request signing primitives.

Use mTLS or a managed workload identity in production when available. This
module provides a small fallback contract for internal adapters and tests.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class SignedRequest:
    key_id: str
    timestamp: int
    nonce: str
    signature: str


def _canonical(method: str, path: str, timestamp: int, nonce: str, body: bytes) -> bytes:
    body_hash = hashlib.sha256(body).hexdigest()
    return f"{method.upper()}\n{path}\n{timestamp}\n{nonce}\n{body_hash}".encode()


def sign_request(key_id: str, secret: bytes, method: str, path: str, body: bytes, *, timestamp: int | None = None, nonce: str) -> SignedRequest:
    if len(secret) < 32:
        raise ValueError("service key must be at least 32 bytes")
    ts = int(time.time()) if timestamp is None else int(timestamp)
    mac = hmac.new(secret, _canonical(method, path, ts, nonce, body), hashlib.sha256).digest()
    return SignedRequest(key_id, ts, nonce, base64.urlsafe_b64encode(mac).decode().rstrip("="))


def verify_request(signed: SignedRequest, secret: bytes, method: str, path: str, body: bytes, *, now: int | None = None, max_skew_seconds: int = 60) -> bool:
    if len(secret) < 32 or not signed.nonce or len(signed.nonce) > 128:
        return False
    current = int(time.time()) if now is None else int(now)
    if abs(current - signed.timestamp) > max_skew_seconds:
        return False
    expected = sign_request(signed.key_id, secret, method, path, body, timestamp=signed.timestamp, nonce=signed.nonce)
    return hmac.compare_digest(expected.signature, signed.signature)
