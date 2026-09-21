"""Optional Neo4j knowledge-graph adapter.

The adapter stores typed, tenant-scoped concepts and relationships. It does
not infer diagnosis or expose raw patient identifiers as graph labels.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GraphNode:
    tenant_id: str
    node_id: str
    kind: str
    attributes: dict[str, Any]


class KnowledgeGraph:
    def __init__(self, uri: str | None = None, username: str | None = None, password: str | None = None):
        self.uri = uri or os.getenv("NEO4J_URL", "")
        self.username = username or os.getenv("NEO4J_USER", "")
        self.password = password or os.getenv("NEO4J_PASSWORD", "")
        self._driver = None
        if self.uri and self.username and self.password:
            try:
                from neo4j import AsyncGraphDatabase
                self._driver = AsyncGraphDatabase.driver(self.uri, auth=(self.username, self.password))
            except ImportError:
                self._driver = None

    @property
    def configured(self) -> bool:
        return self._driver is not None

    async def close(self) -> None:
        if self._driver:
            await self._driver.close()

    async def upsert_node(self, node: GraphNode) -> dict[str, Any]:
        if not node.tenant_id or not node.node_id or not node.kind:
            raise ValueError("tenant_id, node_id and kind are required")
        if not self._driver:
            return {"status": "disabled", "reason": "neo4j_not_configured", "node_id": node.node_id}
        query = ("MERGE (n:Concept {tenant_id: $tenant_id, node_id: $node_id}) "
                 "SET n.kind = $kind, n.attributes = $attributes RETURN n.node_id AS node_id")
        async with self._driver.session() as session:
            result = await session.run(query, tenant_id=node.tenant_id, node_id=node.node_id, kind=node.kind, attributes=node.attributes)
            record = await result.single()
        return {"status": "stored", "node_id": record["node_id"] if record else node.node_id}

    async def relate(self, tenant_id: str, source_id: str, relation: str, target_id: str) -> dict[str, Any]:
        if not all((tenant_id, source_id, relation, target_id)) or not relation.replace("_", "").isalnum():
            raise ValueError("invalid graph relationship")
        if not self._driver:
            return {"status": "disabled", "reason": "neo4j_not_configured"}
        query = ("MATCH (a:Concept {tenant_id: $tenant_id, node_id: $source_id}), "
                 "(b:Concept {tenant_id: $tenant_id, node_id: $target_id}) "
                 "MERGE (a)-[r:RELATED {kind: $relation}]->(b) RETURN r.kind AS kind")
        async with self._driver.session() as session:
            result = await session.run(query, tenant_id=tenant_id, source_id=source_id, target_id=target_id, relation=relation)
            record = await result.single()
        return {"status": "stored", "relation": record["kind"] if record else relation}
