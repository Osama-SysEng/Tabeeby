"""Auditable incident-response state machine; actions are approvals, not exploits."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

TRANSITIONS = {
    "detected": {"triaged"},
    "triaged": {"contained", "false_positive"},
    "contained": {"eradication_in_progress", "recovered"},
    "eradication_in_progress": {"recovered"},
    "recovered": {"closed"},
    "false_positive": {"closed"},
    "closed": set(),
}

@dataclass
class Incident:
    incident_id: str
    severity: str
    state: str = "detected"
    evidence_refs: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    timeline: list[dict] = field(default_factory=list)

    def transition(self, next_state: str, *, actor: str, reason: str) -> None:
        if next_state not in TRANSITIONS.get(self.state, set()):
            raise ValueError(f"invalid incident transition: {self.state} -> {next_state}")
        if not actor or not reason:
            raise ValueError("actor and reason are required")
        self.timeline.append({"from": self.state, "to": next_state, "actor": actor, "reason": reason, "at": datetime.now(timezone.utc).isoformat()})
        self.state = next_state

    def propose_containment(self, *, target: str) -> str:
        if self.state not in {"triaged", "contained"}:
            raise ValueError("containment can only be proposed after triage")
        action = f"isolate:{target}"
        self.actions.append(action)
        return action
