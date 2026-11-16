# NIS2 & DORA Alignment

Source of truth: `data/compliance.json` — run `python tools/ciso.py compliance`.

## NIS2 (Directive (EU) 2022/2555) — readiness 70%

Helios Docs is likely an **important entity**; scope to be confirmed under national transposition.

| Requirement | Status | Score | Owner | Main gap |
|---|---|---:|---|---|
| Art. 20 — Management approval, oversight, training | Partial | 60% | CEO | Board training planned Q1 2027 |
| Art. 21(2)(a) — Risk analysis & policies | Implemented | 85% | CISO | — |
| Art. 21(2)(b) — Incident handling | Partial | 65% | CISO | 24/7 detection pending MDR |
| Art. 21(2)(c) — Continuity, backup, crisis management | Partial | 55% | CIO | SaaS RTO gap (12h vs 4h) |
| Art. 21(2)(d) — Supply chain security | Partial | 45% | COO | 43% of critical suppliers not assessed |
| Art. 21(2)(e) — Secure development & vulnerability handling | Partial | 70% | CTO | Critical vulns within SLA: 82% |
| Art. 21(2)(f) — Effectiveness assessment | Partial | 60% | CISO | External audit planned |
| Art. 21(2)(g) — Cyber hygiene & training | Implemented | 80% | CHRO | — |
| Art. 21(2)(h) — Cryptography | Implemented | 85% | CTO | — |
| Art. 21(2)(i) — HR security, access control, assets | Partial | 65% | CIO | Privileged reviews at 75% |
| Art. 21(2)(j) — MFA & secured communications | Implemented | 90% | CIO | — |
| Art. 23 — Reporting (24h / 72h / 1 month) | Implemented | 80% | CISO | — |

## DORA (Regulation (EU) 2022/2554) — readiness 55%

Applies **indirectly**: financial-sector customers must flow DORA requirements into their ICT contracts.

| Requirement | Status | Score | Owner | Main gap |
|---|---|---:|---|---|
| Art. 30 — Contractual provisions | Partial | 60% | Legal | DORA annex drafted, not yet signed |
| Art. 28(8) — Exit strategies | Partial | 50% | CTO | Exit not tested with a customer |
| Art. 19 — Support customers' incident reporting | Implemented | 80% | CISO | — |
| Art. 11 — ICT business continuity | Partial | 55% | CIO | Second region planned (DEC-008) |
| Art. 24–26 — Resilience testing participation | Planned | 30% | CISO | TLPT participation not organised |

Target: **NIS2 ≥ 85% and DORA ≥ 75% by Q2 2027**, reported quarterly to the board.

_Indicative self-assessment for a portfolio; not legal advice._
