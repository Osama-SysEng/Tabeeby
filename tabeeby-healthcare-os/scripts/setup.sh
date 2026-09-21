#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v docker >/dev/null || { echo "Docker is required" >&2; exit 1; }
docker compose version >/dev/null || { echo "Docker Compose v2 is required" >&2; exit 1; }

if [[ ! -f .env ]]; then
  cp .env.example .env
  chmod 600 .env
  python3 - <<'PY'
from pathlib import Path
import secrets
p = Path('.env')
s = p.read_text()
replacements = {
    'change-me-in-production': secrets.token_hex(32),
    'change-me-encryption-key': secrets.token_hex(64),
    'change-me-db-password': secrets.token_hex(32),
}
for old, new in replacements.items():
    s = s.replace(old, new)
p.write_text(s)
PY
  echo "Created a local .env with random development secrets; it is excluded from release archives."
fi

# Start only data-plane dependencies first.
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up -d postgres timescaledb neo4j qdrant redis minio kafka zookeeper clamav

for i in {1..60}; do
  if docker compose --env-file .env -f infrastructure/docker/docker-compose.yml exec -T postgres pg_isready -U postgres -d tabeeby >/dev/null 2>&1; then break; fi
  sleep 2
done

docker compose --env-file .env -f infrastructure/docker/docker-compose.yml exec -T postgres pg_isready -U postgres -d tabeeby >/dev/null
# Bootstrap scripts are idempotent; do not hide migration errors.
docker compose --env-file .env -f infrastructure/docker/docker-compose.yml exec -T postgres psql -v ON_ERROR_STOP=1 -U postgres -d tabeeby -f /docker-entrypoint-initdb.d/init.sql

echo "Database dependencies are ready. Run the full stack with:"
echo "docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up -d"
