#!/usr/bin/env bash
set -euo pipefail

: "${AUTO_MAINTENANCE_ENABLED:?Set AUTO_MAINTENANCE_ENABLED=true explicitly to enable}"
if [[ "$AUTO_MAINTENANCE_ENABLED" != "true" ]]; then
  echo "automatic maintenance is disabled"
  exit 0
fi
INTERVAL_SECONDS="${MAINTENANCE_INTERVAL_SECONDS:-86400}"
if ! [[ "$INTERVAL_SECONDS" =~ ^[0-9]+$ ]] || (( INTERVAL_SECONDS < 300 )); then
  echo "MAINTENANCE_INTERVAL_SECONDS must be an integer >= 300" >&2
  exit 2
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="${MAINTENANCE_LOCK_FILE:-/tmp/tabeeby-maintenance.lock}"

while true; do
  if command -v flock >/dev/null 2>&1; then
    (
      flock -n 9 || exit 75
      "$ROOT/scripts/maintenance_once.sh"
    ) 9>"$LOCK_FILE" || {
      status=$?
      if [[ "$status" == 75 ]]; then
        echo "maintenance already running; skipping"
      else
        echo "maintenance failed; leaving data unchanged and retrying next interval" >&2
      fi
    }
  else
    "$ROOT/scripts/maintenance_once.sh" || echo "maintenance failed; leaving data unchanged and retrying next interval" >&2
  fi
  sleep "$INTERVAL_SECONDS"
done
