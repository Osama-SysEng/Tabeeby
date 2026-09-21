"""Deterministic, low-noise detection rules for application security events."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import time


@dataclass(frozen=True)
class Alert:
    rule_id: str
    severity: str
    subject: str
    reason: str
    recommended_action: str


class DetectionEngine:
    def __init__(self, window_seconds: int = 300, failed_login_threshold: int = 8):
        self.window_seconds = window_seconds
        self.failed_login_threshold = failed_login_threshold
        self._failures: dict[str, deque[float]] = defaultdict(deque)

    def observe(self, event_type: str, subject: str, *, now: float | None = None, details: dict | None = None) -> list[Alert]:
        current = time.time() if now is None else now
        details = details or {}
        alerts: list[Alert] = []
        if event_type == "auth.failure":
            bucket = self._failures[subject]
            bucket.append(current)
            while bucket and current - bucket[0] > self.window_seconds:
                bucket.popleft()
            if len(bucket) >= self.failed_login_threshold:
                alerts.append(Alert("AUTH-BRUTE-001", "high", subject, "repeated authentication failures in one window", "temporarily block subject and require re-authentication"))
        if event_type in {"authz.denied", "path.traversal", "ssrf.blocked", "upload.malware", "request.replay"}:
            severity = "critical" if event_type in {"upload.malware", "ssrf.blocked"} else "high"
            alerts.append(Alert(f"EVENT-{event_type.upper().replace('.', '-')}", severity, subject, event_type, "quarantine or isolate affected connector and start incident review"))
        if event_type == "rate.limit.exceeded" and details.get("unique_paths", 0) >= 20:
            alerts.append(Alert("RATE-SCAN-001", "medium", subject, "rate-limit violations across many paths", "apply temporary rate reduction and inspect source telemetry"))
        return alerts
