#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?DATABASE_URL is required; no default credentials are allowed}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATIONS_DIR="${MIGRATIONS_DIR:-$ROOT/database/postgres/migrations}"
PSQL=(psql "$DATABASE_URL" -v ON_ERROR_STOP=1)

"${PSQL[@]}" -q -c "CREATE TABLE IF NOT EXISTS schema_migrations (version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now(), checksum text NOT NULL);"

shopt -s nullglob
files=("$MIGRATIONS_DIR"/*.sql)
for file in "${files[@]}"; do
    version="$(basename "$file")"
    checksum="$(sha256sum "$file" | awk '{print $1}')"
    existing="$("${PSQL[@]}" -Atqc "SELECT checksum FROM schema_migrations WHERE version = '$version'")"
    if [[ -n "$existing" ]]; then
        if [[ "$existing" != "$checksum" ]]; then
            echo "checksum mismatch for already-applied migration: $version" >&2
            exit 1
        fi
        echo "already applied: $version"
        continue
    fi

    echo "applying: $version"
    "${PSQL[@]}" -1 \
        -v migration_version="$version" \
        -v migration_checksum="$checksum" \
        -c "SELECT pg_advisory_xact_lock(hashtextextended('tabeeby:migrations', 0));" \
        -f "$file" \
        -c "INSERT INTO schema_migrations(version, checksum) VALUES (:'migration_version', :'migration_checksum');"
done
