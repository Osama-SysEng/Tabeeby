"""Authorization-first, non-exploitative security simulation planner."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class SimulationRequest:
    target: str
    owner_approval: bool
    mode: str = "dry_run"


SAFE_SCENARIOS = (
    "security_headers_review",
    "authentication_boundary_review",
    "authorization_negative_tests",
    "rate_limit_and_body_limit_review",
    "dependency_and_secret_scan",
    "malware_upload_rejection_review",
)


def plan_simulation(request: SimulationRequest) -> dict:
    parsed = urlparse(request.target)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("target must be an HTTP(S) URL")
    if not request.owner_approval:
        raise PermissionError("explicit owner approval is required")
    if request.mode != "dry_run":
        raise ValueError("only dry_run mode is available in this release")
    return {
        "status": "planned_only",
        "target": request.target,
        "scenarios": list(SAFE_SCENARIOS),
        "network_actions_attempted": [],
        "exploit_payloads_sent": False,
        "human_approval": True,
    }
