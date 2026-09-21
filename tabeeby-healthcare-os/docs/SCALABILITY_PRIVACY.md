# Scalability and Privacy Hardening

## Identity with one verified contact

The platform may require one verified email address or one verified phone number per account within a tenant. Normalize the value, verify ownership through the identity provider, compute a keyed lookup digest, and enforce a partial unique database index on `(tenant_id, digest)`. Store the provider subject as the stable identity. Do not place email or phone in URLs, public IDs, logs, analytics labels, or JWT claims. A shared family phone number, hospital switchboard, or delegated caregiver account must be modeled explicitly rather than bypassing uniqueness.

## Doctor and hospital privacy

Every record and query must carry `tenant_id` and, when relevant, `facility_id` and `department_id`. Apply resource-level authorization in the service and database query, not only in the frontend. Keep patient records, clinician profiles, hospital rosters, research datasets, and operational telemetry in separate schemas or stores. Researchers receive approved de-identified datasets only. Redact free-text notes and images from logs, traces, caches, vector payloads, and error responses.

## High-concurrency architecture

Run stateless API gateway and service replicas behind a load balancer. Store sessions, revocation, rate-limit counters, idempotency keys, and job state in shared durable infrastructure. Put imaging analysis, RAG ingestion, exports, and model jobs behind queues with bounded workers, retry budgets, dead-letter queues, and backpressure. Use Redis only for bounded cache/session data with TTL and tenant-scoped keys; use PostgreSQL read replicas and partitioned TimescaleDB tables for durable data; use object storage for large images and documents.

Use per-tenant and per-user quotas, circuit breakers for provider calls, request deadlines, connection pools, bounded pagination, cache invalidation, and admission control. Observe p95/p99 latency, error rate, queue age, database saturation, replication lag, cache hit rate, rejected requests, and cross-tenant authorization denials. Treat any user-count or latency target as unverified until a reproducible load test demonstrates it.

## Safe rollout

Start with a single-facility staging tenant and synthetic data. Enable shadow reads before writes, canary one service replica, test backup restoration, and verify the kill switch. Keep emergency, robot, nano, clinical recommendation, and external notification paths non-actuating until a qualified security/clinical commissioning process approves each adapter.
