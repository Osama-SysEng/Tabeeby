# Defensive Security and Data Admission

## Defensive simulator

The simulator is authorization-first and dry-run only. It produces a plan for security-header review, authentication and authorization negative tests, rate/body-limit review, dependency/secret scanning, and malware-upload rejection. It does not send exploit payloads, probe arbitrary public hosts, or claim that a vulnerability was exploited. An explicit asset-owner approval is required.

## File admission pipeline

Uploads are data, never executable content. The service applies an extension allowlist, filename safety, maximum size, signature and declared-content checks, active PDF-content rejection, ZIP traversal/member/expansion-ratio controls, SHA-256 recording, and quarantine until an antivirus verdict exists. These controls follow a defense-in-depth approach recommended by OWASP [1]. Content-Type alone is not trusted, ZIPs are treated as high-risk containers, and files are not released to application parsers before scanning.

ClamAV is connected through a local Unix socket when configured. Its signature database must be current. A TCP ClamAV socket must not be exposed publicly because the daemon does not authenticate TCP traffic [2]. If ClamAV is unavailable, the service returns `quarantined`, not `clean`.

## Medical source connectors

External university or medical-site connectors must use an exact HTTPS hostname allowlist, bounded response sizes, approved content types, provenance fields, rate limits, and a separate service identity. Protected FHIR exchange must separate authentication, authorization decisions, and audit logging; OAuth/SMART App Launch is the recommended direction for protected FHIR interactions [3]. Consent and security labels must influence access decisions, and cross-organization trust must be explicit.

## Python and network controls

The AST policy rejects dynamic execution and dangerous imports before any code is considered for processing. It is not a sandbox and does not authorize execution of untrusted code. IP handling trusts forwarding headers only from configured proxy CIDRs, and outbound adapters must apply hostname/IP allowlists and block local or link-local targets to reduce SSRF risk.

## References

[1]: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html "OWASP File Upload Cheat Sheet"
[2]: https://docs.clamav.net/manual/Usage/Scanning.html "ClamAV Scanning Documentation"
[3]: https://hl7.org/fhir/security.html "HL7 FHIR Security"

## Monitoring, detection, and response

The gateway now emits structured security events for denied authentication and rate-limit violations, with redaction of passwords, tokens, authorization values, contact identifiers, and clinical fields. `DetectionEngine` detects repeated authentication failures, malware/SSRF/path-traversal/replay indicators, and broad rate-limit scanning patterns. `Incident` enforces an auditable sequence from detection to triage, containment, eradication, recovery, and closure.

The repository also contains a scheduled CodeQL workflow with security-extended queries and dependency auditing. Findings must be reviewed by an authorized security owner; automated remediation must not patch production blindly. Containment proposals are reversible or approval-gated, and no component performs offensive probing or exploit delivery.
