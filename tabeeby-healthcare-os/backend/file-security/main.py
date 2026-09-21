from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

_shared_root = str(Path(__file__).resolve().parents[1])
if _shared_root not in sys.path:
    sys.path.insert(0, _shared_root)
from shared.security.file_safety import clamd_scan_stream, inspect_upload, inspect_zip_container

app = FastAPI(title="Tabeeby File Security", version="1.0.0")
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
CLAMD_SOCKET = os.getenv("CLAMD_SOCKET", "")


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy", "service": "file-security", "scan_backend": "clamd" if CLAMD_SOCKET else "not_configured"}


@app.post("/api/v1/files/scan")
async def scan_file(file: UploadFile = File(...)) -> dict:
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="upload exceeds configured size limit")
    verdict = inspect_upload(file.filename or "", data, declared_content_type=file.content_type, max_bytes=MAX_UPLOAD_BYTES)
    if verdict.reason == "extension_not_allowed" and (file.filename or "").lower().endswith(".zip"):
        verdict = inspect_zip_container(data)
    if not verdict.accepted:
        raise HTTPException(status_code=422, detail={"status": "rejected", "reason": verdict.reason, "sha256": verdict.sha256})
    if not CLAMD_SOCKET:
        return {"status": "quarantined", "reason": "malware_scanner_not_configured", "sha256": verdict.sha256, "detected_type": verdict.detected_type}
    try:
        malware_scan = clamd_scan_stream(data, socket_path=CLAMD_SOCKET)
    except OSError:
        return {"status": "quarantined", "reason": "malware_scanner_unavailable", "sha256": verdict.sha256, "detected_type": verdict.detected_type}
    if malware_scan != "clean":
        raise HTTPException(status_code=422, detail={"status": "rejected", "reason": "malware_scan_failed", "scan": malware_scan, "sha256": verdict.sha256})
    return {"status": "clean", "reason": "accepted_after_antivirus_scan", "sha256": verdict.sha256, "detected_type": verdict.detected_type}
