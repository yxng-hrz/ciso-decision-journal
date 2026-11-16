# Post-Incident Executive Report — Ransomware (February 2026)

## What worked

- **Immutable, tested backups** — full restoration without paying.
- **Crisis governance** — decisions in hours, single voice to customers and regulators.
- **Regulatory readiness** — NIS2 24h / 72h / 1-month milestones met.

## What failed

| Finding | Root cause | Corrective action | Owner | Status |
|---|---|---|---|---|
| 9-hour detection delay | No 24/7 monitoring (accepted risk A1/A2) | MDR service (DEC-007) | CISO | In progress |
| Initial access via contractor without MFA | Undated legacy exception | Exceptions now time-bound; MFA 98% | CIO | Done |
| RTO exceeded (52h vs 4h target) | Single-region architecture | Warm standby (DEC-008) | CTO | Planned |
| Contractor security not assessed | No TPRM process | Supplier assessments; contract clauses | COO | In progress |

## Executive requests

1. Approve the MDR contract (€85k/year, ROSI ≈ 84%).
2. Fund the warm standby (€120k/year) to meet the 4h RTO promised to customers.
3. Make supplier security assessment a procurement prerequisite.
