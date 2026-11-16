# Incident Response Case — Ransomware on Production (February 2026)

## Scenario

A compromised contractor VPN account (no MFA — legacy exception) is used to deploy ransomware on part of the production environment. Customer document access is degraded for 2 days.

## Timeline and regulatory clock

| Time | Event | Decision / obligation |
|---|---|---|
| D0 22:40 | EDR alert on mass file encryption, outside business hours | No 24/7 monitoring: alert seen at 07:30 (R9) |
| D1 07:45 | Encryption confirmed on 14 servers | CISO activates incident command |
| D1 09:00 | Crisis committee (CEO, CIO, CISO, CTO, DPO, Legal, Comms) | Isolate segments, preserve evidence |
| D1 10:30 | Exfiltration cannot be excluded | GDPR 72h clock and **NIS2 24h early warning** started |
| D1 21:00 | NIS2 early warning sent to the CSIRT | Within 24h of awareness |
| D2 | Restoration from immutable backups begins | **No ransom payment**; law enforcement notified |
| D3 | Service restored; customers informed (DEC-005) | NIS2 incident notification within 72h; GDPR notification to the DPA |
| D+30 | Final report to the CSIRT | Root cause, measures, cross-border impact |

## Key decisions

- **No ransom**: backups were intact and tested; payment would fund crime and guarantee nothing.
- **Transparent communication** within regulatory deadlines (DEC-005).
- **Contractor MFA exception closed** the same week; legacy exceptions now expire automatically.

## Outcome

Operations restored in 52 hours, no data published, no churn attributed to the incident. Lessons in `post-incident-executive-report.md`.
