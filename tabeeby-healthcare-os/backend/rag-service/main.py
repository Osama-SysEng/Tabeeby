from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tabeeby RAG Service", version="1.0.0")


@dataclass(frozen=True)
class RetrievalConfig:
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    ollama_url: str = os.getenv("OLLAMA_URL", "")
    enabled: bool = os.getenv("RAG_ENABLED", "false").casefold() == "true"


class QueryRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=120)
    query: str = Field(min_length=3, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)


@app.get("/health")
async def health() -> dict[str, Any]:
    config = RetrievalConfig()
    return {"status": "healthy", "service": "rag-service", "mode": "enabled" if config.enabled else "disabled", "qdrant_configured": bool(config.qdrant_url), "ollama_configured": bool(config.ollama_url)}


@app.post("/api/v1/rag/query")
async def query(request: QueryRequest) -> dict[str, Any]:
    config = RetrievalConfig()
    if not config.enabled or not config.qdrant_url or not config.ollama_url:
        raise HTTPException(status_code=503, detail="RAG connector is disabled or incomplete; no clinical answer generated")
    # The production adapter must enforce tenant filters, provenance, consent,
    # timeouts, citation return, and a human review boundary before generation.
    return {"status": "connector_contract_ready", "tenant_id": request.tenant_id, "query": request.query, "top_k": request.top_k, "citations": [], "answer": None, "clinical_decision": False}
