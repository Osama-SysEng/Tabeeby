#!/usr/bin/env bash
set -euo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"
BACKUP_DIR="${BACKUP_DIR:-$ROOT/.local-backups/$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "$BACKUP_DIR"

compose=(docker compose --env-file .env -f infrastructure/docker/docker-compose.yml)
pg_dump_service() {
  local service="$1" database="$2" output="$3"
  "${compose[@]}" exec -T -e PGPASSWORD="$POSTGRES_PASSWORD" "$service" pg_dump --no-owner --no-privileges -U postgres "$database" > "$output"
}

pg_dump_service postgres tabeeby "$BACKUP_DIR/postgres.sql"
pg_dump_service timescaledb tabeeby_iot "$BACKUP_DIR/timescale.sql"
"${compose[@]}" exec -T neo4j neo4j-admin dump --to=/tmp/neo4j.dump
"${compose[@]}" cp neo4j:/tmp/neo4j.dump "$BACKUP_DIR/neo4j.dump"
"${compose[@]}" exec -T redis redis-cli --raw BGSAVE >/dev/null
"${compose[@]}" cp redis:/data/dump.rdb "$BACKUP_DIR/redis.rdb"
"${compose[@]}" exec -T qdrant tar czf /tmp/qdrant-storage.tar.gz /qdrant/storage
"${compose[@]}" cp qdrant:/tmp/qdrant-storage.tar.gz "$BACKUP_DIR/qdrant-storage.tar.gz"

find "$BACKUP_DIR" -type f -printf '%P\n' | sort | xargs -r sha256sum > "$BACKUP_DIR/SHA256SUMS"
printf 'backup_dir=%s\n' "$BACKUP_DIR"
printf 'restore_required=true\n'
printf 'Restore tests must be executed in a disposable environment before declaring a recovery point valid.\n'
