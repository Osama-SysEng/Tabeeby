"""Deterministic physician assignment helper; not a clinical decision engine."""
from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass


@dataclass(frozen=True)
class PhysicianAssignment:
    tenant_id: str
    patient_id: str
    physician_id: str
    assignment_version: str = "v1"


def assign_lifetime_physician(tenant_id: str, patient_id: str, physician_ids: list[str], secret: bytes) -> PhysicianAssignment:
    if not tenant_id or not patient_id or not physician_ids or len(secret) < 32:
        raise ValueError("tenant, patient, physicians, and a 32-byte assignment key are required")
    if any(not physician_id for physician_id in physician_ids):
        raise ValueError("physician IDs must be non-empty")
    digest = hmac.new(secret, f"{tenant_id}:{patient_id}".encode(), hashlib.sha256).digest()
    selected = physician_ids[int.from_bytes(digest[:8], "big") % len(physician_ids)]
    return PhysicianAssignment(tenant_id, patient_id, selected)
