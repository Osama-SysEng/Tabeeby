# Tabeeby Healthcare OS — Hardened Prototype Release

## Release scope

This release is a **simulation-first, non-clinical prototype**. It improves safety boundaries, local buildability, configuration hygiene, and testability. It does not implement or validate the medical, surgical, nano, biological, emergency-dispatch, or national-scale claims in the supplied long-term brief.

## Changes in this release

| Area | Change | Verification |
|---|---|---|
| Emergency workflow | Replaced canned autonomous dispatch statuses with draft-only, non-actuating responses and explicit human approval fields. | Safety unit test passes. |
| Nano control | Live molecular execution endpoint returns a controlled `409 LIVE_ACTUATION_DISABLED` response. | Safety unit test passes. |
| Robot control | Hardware scan/firmware and override responses are simulation-only and record that no external action was attempted. | Static marker scan and import checks pass. |
| Authentication | JWT secret is environment-configured; production fails closed when absent; login requires an explicitly enabled development identity stub. | Import and permission contract tests pass. |
| Patient contracts | Added bounded field validation, safe list defaults, and path/body patient identity matching for vitals. | Unit and safety tests pass. |
| Infrastructure | Removed committed secret values, parameterized database credentials, corrected service URL wiring, and fixed Compose build contexts and bind-mount paths. | Static secret scan passes; Compose was not executed because Docker is unavailable in the sandbox. |
| Web interface | Replaced unsupported marketing metrics with a readiness dashboard that labels simulation, sandbox, disabled, and non-clinical states. | `npm run build` passes with Next.js 16.3.3. |
| Documentation | Added operating and security-boundary guidance and a sanitized `.env.example`. | Files included in archive. |

## Verification record

The final verification run produced the following results:

| Check | Result |
|---|---|
| Python syntax compilation for backend and edge code | Passed |
| Python unit and safety tests | 8 tests passed |
| Web dependency installation | Passed after correcting unavailable/ incompatible package versions |
| Web production build | Passed; routes `/` and `/_not-found` prerendered |
| Hardcoded secret scan | No matching committed secret values after remediation |
| Docker Compose validation | Not executed because Docker is not installed in the verification environment |

Warnings about deprecated `datetime.utcnow()` and Pydantic `.dict()` remain in legacy prototype services and should be addressed in a future compatibility pass.

## Activation gates

Do not connect real patients, medical devices, hospitals, ambulances, robots, molecular tools, notification providers, or government systems to this archive. Any future activation requires qualified clinical and security review, validated datasets and models, approved identity and consent systems, durable encrypted storage, observability, incident response, disaster recovery, regulatory assessment, and commissioning of every external adapter.

## Follow-up hardening

The follow-up pass adds a privacy-preserving identity helper, a PostgreSQL schema with tenant-scoped unique email/phone lookup digests, a Compose scale overlay for stateless services, and a scalability/privacy guide. The identity tests verify normalization, E.164-like phone input, keyed HMAC lookup, and minimum key length. The full Python suite now passes 11 tests.

## Defensive security controls

This round adds an AST-based Python safety policy that rejects dynamic execution, dangerous imports, introspection, and oversized snippets without executing supplied code. It adds trusted-proxy-aware client IP resolution, rejects unsafe local endpoint targets for outbound adapters, applies gateway request-size limits and security headers, strips client-controlled forwarding and authorization headers before proxying, and passes only gateway-derived internal identity metadata. It also adds HMAC request signing with timestamp skew and nonce checks for service-to-service adapters.

The full Python suite now passes 16 tests. Docker image builds and runtime startup remain dependent on a local Docker installation and were not executed in this environment.

## Database growth and scheduled maintenance

Added PostgreSQL and TimescaleDB bootstrap schemas, numbered PostgreSQL migrations with checksum verification and transactional advisory locking, auditable maintenance/source-cursor state, and bounded time-series indexes/retention foundations. Added `scripts/migrate.sh`, a fail-closed `scripts/backup.sh` with SHA-256 manifest, `scripts/maintenance_once.sh` that backs up before migrations and runs ANALYZE, and an opt-in `scripts/maintenance_loop.sh` with a minimum five-minute interval and single-run lock. Automatic maintenance is disabled by default and must be scheduled on a controlled host after staging and restore tests.

The architecture comparison references Alembic for reviewed versioned migrations, Airflow for idempotent retryable tasks, and pgBackRest for encrypted, retention-managed backups and WAL recovery. Runtime database migrations and Docker Compose startup were not executed in this environment.

## Security observability and response

Added structured privacy-preserving security telemetry, deterministic detection rules for repeated authentication failures, rate-limit scanning, SSRF/path traversal/replay/malware indicators, and an auditable incident-response state machine. Added a scheduled CodeQL security-extended and dependency-audit workflow. Added the missing Tabeeby contracts for Neo4j knowledge graphs, RAG connectors, imaging inference, molecular descriptors, virtual physician assignment, seven-step non-actuating emergency planning, and a physician dashboard. Optional adapters remain disabled or non-clinical until their validated dependencies, credentials, datasets, and commissioning gates exist.

The latest local verification run passes 25 Python tests, Python compilation, and Bash syntax checks. Runtime Docker, database, and external integrations were not executed in this environment.
