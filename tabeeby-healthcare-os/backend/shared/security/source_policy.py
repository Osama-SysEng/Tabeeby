"""Allowlist and provenance policy for medical information connectors."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from .ip_policy import reject_public_endpoint_target


@dataclass(frozen=True)
class ApprovedSource:
    source_id: str
    hostname: str
    organization: str
    allowed_content_types: tuple[str, ...] = ("application/json", "application/fhir+json", "text/xml")
    max_bytes: int = 5 * 1024 * 1024


def validate_source_url(url: str, source: ApprovedSource) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or not parsed.hostname:
        raise ValueError("source must use HTTPS without embedded credentials")
    hostname = parsed.hostname.casefold().rstrip(".")
    if hostname != source.hostname.casefold().rstrip("."):
        raise PermissionError("source hostname is not approved")
    reject_public_endpoint_target(hostname)
    return parsed.geturl()


def validate_source_response(content_type: str | None, content_length: int | None, source: ApprovedSource) -> None:
    normalized = (content_type or "").split(";", 1)[0].strip().casefold()
    if normalized not in {item.casefold() for item in source.allowed_content_types}:
        raise ValueError("source content type is not approved")
    if content_length is not None and (content_length < 0 or content_length > source.max_bytes):
        raise ValueError("source response exceeds configured limit")
