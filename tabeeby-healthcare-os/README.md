# Tabeeby Healthcare OS

Tabeeby is a **simulation-first healthcare software prototype** for exploring patient workflows, clinical knowledge integration, device telemetry, and safety-aware service boundaries. This repository is not a medical device, is not a diagnostic system, and must not be used to make clinical decisions or contact emergency services.

## What is included

| Area | Current release behavior |
|---|---|
| Patient service | In-memory prototype registration, vitals validation, lifetime-assistant demonstration, and explicit simulation labels |
| Authentication | JWT contract with environment-configured secret; login remains disabled unless an explicit development identity stub is enabled |
| Emergency workflow | Draft preparation only; no ambulance, hospital, device, physician, or emergency-contact delivery is attempted |
| Diagnostic and research services | Prototype/simulation components requiring real datasets, model evaluation, provenance, and qualified review |
| Robot and nano services | Hardware/profile simulation and planning only; live actuation is disabled |
| Web frontend | Readiness dashboard that distinguishes available, sandbox, simulation, and disabled modules |
| Infrastructure | Docker Compose, Kubernetes, Terraform, data-store configuration, and security policy examples requiring environment-specific commissioning |

## Quick start

Copy `.env.example` to `.env` and replace every placeholder with locally managed values. Never commit `.env`, production credentials, patient data, device keys, or provider tokens. The local stack is intended for isolated development and must be treated as non-production until identity, storage, observability, networking, backup, compliance, and commissioning controls are reviewed.

```bash
cp .env.example .env
# set POSTGRES_PASSWORD, NEO4J_PASSWORD, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD,
# JWT_SECRET_KEY, and ENCRYPTION_KEY in .env

docker compose --env-file .env -f infrastructure/docker/docker-compose.yml config
# Start only after reviewing the generated configuration:
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up --build
```

The web application is exposed at `http://localhost:3000` in the development Compose configuration. Infrastructure ports should not be exposed beyond an isolated development network.

## Tests and checks

```bash
python3 -m compileall -q backend edge-computing
python3 -m unittest discover -s tests -p 'test_*.py'
cd frontend/web
npm install
npm run build
```

The current release includes focused safety tests covering emergency non-actuation, nano execution rejection, patient input validation, and patient/vitals identity matching. A successful build is not evidence of clinical validity, regulatory approval, or production readiness.

## Safety and deployment boundaries

All external integrations are disabled by default. Emergency notifications, device control, robot control, molecular operations, clinical recommendations, and data sharing require separate adapters, authenticated identities, consent and audit controls, idempotency, monitoring, a kill switch, and qualified human commissioning. The current implementation deliberately returns `simulation_only`, `non_actuating`, or `prepared_not_sent` states where an earlier prototype claimed live execution.

The Kubernetes Secret manifest contains empty values intentionally. Inject secrets through an approved secret manager or sealed-secret workflow. Do not deploy the checked-in manifest as a source of production secrets.

See `docs/SECURITY_BOUNDARIES.md`, `docs/development/setup.md`, and `docs/api/openapi.yaml` for additional guidance. The 53-item brief remains a long-term research specification; it is not a statement that those capabilities are implemented in this archive.
