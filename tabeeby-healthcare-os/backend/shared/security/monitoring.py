"""Structured security telemetry with privacy-preserving redaction."""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Any

SENSITIVE_KEYS = frozenset({"password", "token", "authorization", "secret", "email", "phone", "patient_name", "ssn", "medical_record"})


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): ("[REDACTED]" if str(k).casefold() in SENSITIVE_KEYS else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value[:100]]
    if isinstance(value, str) and len(value) > 2000:
        return value[:2000] + "...[TRUNCATED]"
    return value


@dataclass(frozen=True)
class SecurityEvent:
    event_type: str
    outcome: str
    request_id: str
    occurred_at: float
    tenant_id: str | None = None
    actor_id: str | None = None
    client_ip: str | None = None
    details: dict[str, Any] | None = None

    def to_json(self) -> str:
        payload = asdict(self)
        payload["details"] = redact(payload.get("details") or {})
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def make_security_event(event_type: str, outcome: str, *, request_id: str | None = None, tenant_id: str | None = None, actor_id: str | None = None, client_ip: str | None = None, details: dict[str, Any] | None = None) -> SecurityEvent:
    if not event_type or not outcome:
        raise ValueError("event_type and outcome are required")
    return SecurityEvent(event_type, outcome, request_id or str(uuid.uuid4()), time.time(), tenant_id, actor_id, client_ip, details)
