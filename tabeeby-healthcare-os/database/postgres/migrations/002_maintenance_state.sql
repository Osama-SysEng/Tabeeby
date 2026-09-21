-- Migration 002: auditable refresh state and idempotent source cursors.
CREATE TABLE IF NOT EXISTS maintenance_runs (
    run_id text PRIMARY KEY,
    job_name text NOT NULL,
    status text NOT NULL CHECK (status IN ('started','succeeded','failed')),
    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz,
    details jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS source_cursors (
    source_id text PRIMARY KEY,
    cursor_value text,
    last_success_at timestamptz,
    checksum text,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS maintenance_runs_job_time_idx ON maintenance_runs (job_name, started_at DESC);
