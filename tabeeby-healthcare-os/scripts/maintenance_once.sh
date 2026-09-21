#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
: "${DATABASE_URL:?DATABASE_URL is required}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"

# Never mutate schema before a backup attempt has completed.
BACKUP_DIR="${BACKUP_DIR:-$ROOT/.local-backups/$(date -u +%Y%m%dT%H%M%SZ)}"
BACKUP_DIR="$BACKUP_DIR" ./scripts/backup.sh
DATABASE_URL="$DATABASE_URL" ./scripts/migrate.sh

# Statistics maintenance is bounded and deterministic; it does not delete data.
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -c 'ANALYZE;'

run_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 \
  -v run_id="$run_id" \
  -c "INSERT INTO maintenance_runs(run_id, job_name, status, finished_at) VALUES (:'run_id', 'database-maintenance', 'succeeded', now());"
echo "maintenance_status=succeeded run_id=$run_id"
