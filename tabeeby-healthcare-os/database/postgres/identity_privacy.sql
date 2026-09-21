-- Privacy-preserving identity foundation.
-- Raw contact values belong in an approved identity provider or encrypted vault.
-- Only keyed digests are used for uniqueness and lookup.

CREATE TABLE IF NOT EXISTS tenant_users (
    user_id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    facility_id UUID,
    identity_provider TEXT NOT NULL,
    provider_subject TEXT NOT NULL,
    email_lookup_digest CHAR(64),
    phone_lookup_digest CHAR(64),
    email_verified_at TIMESTAMPTZ,
    phone_verified_at TIMESTAMPTZ,
    role TEXT NOT NULL CHECK (role IN ('patient', 'physician', 'researcher', 'bioinfo', 'surgeon', 'hospital_admin', 'platform_admin')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('pending', 'active', 'suspended', 'deleted')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (identity_provider, provider_subject)
);

CREATE UNIQUE INDEX IF NOT EXISTS tenant_users_email_unique
    ON tenant_users (tenant_id, email_lookup_digest)
    WHERE email_lookup_digest IS NOT NULL AND status <> 'deleted';

CREATE UNIQUE INDEX IF NOT EXISTS tenant_users_phone_unique
    ON tenant_users (tenant_id, phone_lookup_digest)
    WHERE phone_lookup_digest IS NOT NULL AND status <> 'deleted';

CREATE INDEX IF NOT EXISTS tenant_users_facility_idx
    ON tenant_users (tenant_id, facility_id, role, status);

COMMENT ON TABLE tenant_users IS 'Use provider subject and keyed contact digests; never expose email/phone as public IDs.';
