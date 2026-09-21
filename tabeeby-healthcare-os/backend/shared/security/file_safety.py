"""Defense-in-depth file admission checks.

Files are data, never code. A file must remain quarantined until all checks
pass and an antivirus/ sandbox verdict is available. This module never opens
or executes an uploaded file with an application parser.
"""
from __future__ import annotations

import hashlib
import io
import socket
import struct
import zipfile
from dataclasses import dataclass
from pathlib import PurePath


@dataclass(frozen=True)
class FileVerdict:
    accepted: bool
    reason: str
    sha256: str
    detected_type: str | None = None
    malware_scan: str = "not_run"


ALLOWED_SIGNATURES = {
    ".png": (b"\x89PNG\r\n\x1a\n", "image/png"),
    ".jpg": (b"\xff\xd8\xff", "image/jpeg"),
    ".jpeg": (b"\xff\xd8\xff", "image/jpeg"),
    ".pdf": (b"%PDF-", "application/pdf"),
}


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect_upload(filename: str, data: bytes, *, declared_content_type: str | None = None, max_bytes: int = 10 * 1024 * 1024) -> FileVerdict:
    digest = _digest(data)
    if not filename or len(filename) > 160 or filename.startswith((".", "-")) or ".." in PurePath(filename).parts:
        return FileVerdict(False, "unsafe_filename", digest)
    suffix = PurePath(filename).suffix.casefold()
    signature = ALLOWED_SIGNATURES.get(suffix)
    if signature is None:
        return FileVerdict(False, "extension_not_allowed", digest)
    if len(data) == 0 or len(data) > max_bytes:
        return FileVerdict(False, "size_limit", digest, signature[1])
    if not data.startswith(signature[0]):
        return FileVerdict(False, "signature_mismatch", digest, signature[1])
    if declared_content_type and declared_content_type != signature[1]:
        return FileVerdict(False, "content_type_mismatch", digest, signature[1])
    if suffix == ".pdf" and b"/JavaScript" in data[:2 * 1024 * 1024]:
        return FileVerdict(False, "active_pdf_content", digest, signature[1])
    return FileVerdict(True, "awaiting_malware_scan", digest, signature[1], "required")


def inspect_zip_container(data: bytes, *, max_members: int = 100, max_uncompressed_bytes: int = 50 * 1024 * 1024, max_ratio: int = 100) -> FileVerdict:
    digest = _digest(data)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            total = sum(max(0, member.file_size) for member in members)
            if len(members) > max_members or total > max_uncompressed_bytes:
                return FileVerdict(False, "archive_expansion_limit", digest, "application/zip")
            for member in members:
                if member.filename.startswith(("/", "\\")) or ".." in PurePath(member.filename).parts:
                    return FileVerdict(False, "archive_path_traversal", digest, "application/zip")
                if member.compress_size and member.file_size // max(member.compress_size, 1) > max_ratio:
                    return FileVerdict(False, "archive_compression_ratio", digest, "application/zip")
    except (zipfile.BadZipFile, OSError, ValueError):
        return FileVerdict(False, "invalid_archive", digest, "application/zip")
    return FileVerdict(True, "awaiting_malware_scan", digest, "application/zip", "required")


def clamd_scan_stream(data: bytes, *, socket_path: str = "/var/run/clamav/clamd.ctl", timeout_seconds: float = 5.0) -> str:
    """Ask a local Unix clamd socket to scan bytes; never expose TCP clamd."""
    if len(data) > 25 * 1024 * 1024:
        return "rejected_size"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(timeout_seconds)
        client.connect(socket_path)
        client.sendall(b"zINSTREAM\0")
        offset = 0
        while offset < len(data):
            chunk = data[offset:offset + 1024 * 1024]
            client.sendall(struct.pack(">I", len(chunk)) + chunk)
            offset += len(chunk)
        client.sendall(struct.pack(">I", 0))
        result = client.recv(4096).decode("utf-8", "replace").strip()
    return "clean" if result.endswith("OK") else "infected_or_error"
