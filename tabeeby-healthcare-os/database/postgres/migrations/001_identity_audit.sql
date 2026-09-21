-- Migration 001: tenant-scoped identity and audit foundation.
-- Review with a DBA before applying to any production database.
CREATE TABLE IF NOT EXISTS tenant_users (
    user_id uuid PRIMARY KEY,
    tenant_id uuid NOT NULL,
    facility_id uuid,
    identity_provider text NOT NULL,
    provider_subject text NOT NULL,
    email_lookup_digest char(64),
    phone_lookup_digest char(64),
    email_verified_at timestamptz,
    phone_verified_at timestamptz,
    role text NOT NULL CHECK (role IN ('patient','physician','researcher','bioinfo','surgeon','hospital_admin','platform_admin')),
    status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','active','suspended','deleted')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (identity_provider, provider_subject)
);
CREATE UNIQUE INDEX IF NOT EXISTS tenant_users_email_unique ON tenant_users (tenant_id, email_lookup_digest) WHERE email_lookup_digest IS NOT NULL AND status <> 'deleted';
CREATE UNIQUE INDEX IF NOT EXISTS tenant_users_phone_unique ON tenant_users (tenant_id, phone_lookup_digest) WHERE phone_lookup_digest IS NOT NULL AND status <> 'deleted';
CREATE INDEX IF NOT EXISTS tenant_users_facility_idx ON tenant_users (tenant_id, facility_id, role, status);

CREATE TABLE IF NOT EXISTS security_audit_events (
    event_id uuid PRIMARY KEY,
    tenant_id uuid,
    actor_user_id uuid,
    action text NOT NULL CHECK (length(action) BETWEEN 1 AND 120),
    resource_type text NOT NULL CHECK (length(resource_type) BETWEEN 1 AND 120),
    resource_id text,
    outcome text NOT NULL CHECK (outcome IN ('allowed','denied','error')),
    request_id text,
    occurred_at timestamptz NOT NULL DEFAULT now(),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS security_audit_tenant_time_idx ON security_audit_events (tenant_id, occurred_at DESC);
