# Scaling — Tabeeby (api-gateway + services)

## Workers
- All `backend/*/Dockerfile` already run uvicorn with `--workers 2–8`
  (gateway 4, ultra-iq-engine 8). No change needed.

## Rate limiting
- Already present at `backend/api-gateway/main.py::rate_limit_check`
  (per-tier budgets: patient 100, physician 1000, researcher 5000). No
  change needed.

## Pagination (default 50 / max 500)
- `GET /patients?limit=&offset=` — previously returned the **entire**
  dict as a bare list; now returns
  `{items, total, limit, offset}`. Migration note: clients doing
  `len(resp)` / iterating the body must switch to `resp["items"]`.
- `GET /patients/{id}/vitals?limit=&offset=` — previously unbounded
  history array; now sliced, `history_count` still reports the full total.
- Other services expose per-object routes (no bulk lists found); nothing
  else to paginate without inventing endpoints.

## Remaining capacity limits (honest)
- `patient-service` uses **in-memory** dicts (`patients_db`,
  `vitals_history`): data loss on restart, no cross-worker sharing despite
  `--workers 4`. Postgres/Redis required before real scale-out.
- Gateway rate limiter is Redis-backed when configured, else permissive —
  verify `REDIS_URL` in production.
- Imaging/AI services are compute-bound; workers help I/O only.
