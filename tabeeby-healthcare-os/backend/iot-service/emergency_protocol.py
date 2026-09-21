"""Seven-step emergency workflow planner.

All steps are non-actuating. Real dispatch/device control requires a separately
commissioned adapter, consent, human approval, and operational certification.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


STEPS = (
    "validate_signal",
    "deduplicate_event",
    "classify_severity_advisory",
    "request_human_review",
    "prepare_draft_notification",
    "record_audit_event",
    "close_or_escalate_manually",
)


@dataclass(frozen=True)
class EmergencyPlan:
    incident_id: str
    status: str
    steps: tuple[str, ...]
    external_actions_attempted: tuple[str, ...]
    created_at: str


def build_emergency_plan(incident_id: str, *, human_approved: bool = False) -> EmergencyPlan:
    if not incident_id or len(incident_id) > 120:
        raise ValueError("incident_id is required and bounded")
    if not human_approved:
        return EmergencyPlan(incident_id, "awaiting_human_review", STEPS, (), datetime.now(timezone.utc).isoformat())
    return EmergencyPlan(incident_id, "draft_ready_non_actuating", STEPS, (), datetime.now(timezone.utc).isoformat())
