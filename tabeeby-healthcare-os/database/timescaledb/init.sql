-- TABEEBY IoT Time-Series Data
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS iot_vitals (
    time TIMESTAMPTZ NOT NULL,
    patient_id UUID,
    device_id VARCHAR(100),
    heart_rate FLOAT,
    blood_pressure_systolic FLOAT,
    blood_pressure_diastolic FLOAT,
    spo2 FLOAT,
    temperature FLOAT,
    blood_glucose FLOAT,
    respiratory_rate FLOAT,
    sleep_stage VARCHAR(50),
    activity_level VARCHAR(50),
    hydration_index FLOAT,
    ecg_data JSONB,
    eeg_data JSONB
);

SELECT create_hypertable('iot_vitals', 'time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_iot_patient_time ON iot_vitals(patient_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_iot_device ON iot_vitals(device_id, time DESC);

-- Continuous aggregates
CREATE MATERIALIZED VIEW IF NOT EXISTS iot_vitals_hourly
WITH (timescaledb.continuous) AS
SELECT
    patient_id,
    time_bucket('1 hour', time) AS bucket,
    AVG(heart_rate) AS avg_heart_rate,
    AVG(blood_pressure_systolic) AS avg_bp_sys,
    AVG(blood_pressure_diastolic) AS avg_bp_dia,
    AVG(spo2) AS avg_spo2,
    AVG(temperature) AS avg_temp,
    COUNT(*) AS reading_count
FROM iot_vitals
GROUP BY patient_id, bucket;

-- Retention policy
SELECT add_retention_policy('iot_vitals', INTERVAL '2 years', if_not_exists => TRUE);
