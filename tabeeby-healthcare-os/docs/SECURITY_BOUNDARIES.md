# Security and Operational Boundaries

## Release classification

This repository is a **non-clinical research and integration prototype**. It is suitable for local development, contract testing, interface demonstrations, and simulation workflows. It is not evidence of clinical efficacy, regulatory clearance, diagnostic accuracy, emergency-service reliability, robotic safety, or medical-device compliance.

## Non-actuating policy

The emergency, robot, nano, and surgical paths must remain non-actuating in this release. A response that contains `simulation_only`, `non_actuating`, `prepared_not_sent`, or `external_actions_attempted: []` means that no external provider, hospital, ambulance, patient device, robot, biological system, or molecular tool was contacted or controlled.

Any future adapter for an external action must be introduced behind an explicit feature flag and kill switch. It must require an authenticated service identity, an authorization decision, patient consent where applicable, an idempotency key, replay protection, audit logging, bounded retries, a dead-letter path, monitoring, and qualified human approval. The adapter must expose a verifiable delivery result rather than treating an HTTP response as proof of real-world completion.

## Data and privacy

Do not place real patient data, genomic data, medical images, device identifiers, credentials, tokens, or private keys in this repository, test fixtures, logs, ZIP archives, or browser bundles. The current patient service uses in-memory state and must not be interpreted as durable or compliant clinical storage. A production design requires a reviewed data classification, retention schedule, access policy, consent model, encryption and key management, backup/restore testing, deletion workflow, and jurisdiction-specific compliance review.

## Identity and authorization

JWT secrets are loaded from the environment and production startup fails when the secret is absent. The development login path is disabled unless `TABEEBY_DEV_AUTH=true` and explicit development credentials are configured. This is not a substitute for an OIDC provider, MFA, session revocation, role and resource authorization, or privileged-action approval.

## Model and clinical claims

The diagnostic, RAG, drug-discovery, surgical, quantum, biological, and self-learning modules contain prototype behavior. Random values, fixed confidence numbers, synthetic findings, or canned text must never be presented as validated clinical measurements. Production model work requires representative datasets, data provenance, leakage controls, calibration, subgroup evaluation, uncertainty reporting, drift monitoring, reproducible versioning, independent review, and a documented human decision process.

## Deployment gate

Before any staging or production activation, a qualified security and clinical engineering team must review threat models, API contracts, secrets, network exposure, dependency provenance, incident response, disaster recovery, audit integrity, accessibility, and regulatory obligations. No command in this repository should be treated as authorization to deploy a clinical system.
