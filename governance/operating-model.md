# Security Operating Model — CISO & CIO (RSSI / DSI)

The model separates **who runs IT** (CIO / DSI), **who governs cyber risk** (CISO / RSSI) and **who owns the business risk** (executives).

## RACI

| Activity | CEO / COMEX | CIO (DSI) | CISO (RSSI) | CTO | DPO | Business owners |
|---|---|---|---|---|---|---|
| Cyber risk appetite & acceptance | **A** | C | R | C | C | R |
| Security policy & baselines | I | C | **A/R** | C | C | I |
| IT run, patching, backups | I | **A/R** | C | R | I | I |
| Identity & access governance | I | **A** | R (control) | R | C | R (reviews) |
| Product / application security | I | C | R | **A** | C | I |
| Incident command | I | R | **A/R** | R | R | C |
| Regulatory notification (NIS2, GDPR) | **A** | C | R | C | R | I |
| Business continuity (BIA, DRP) | **A** | R | C | R | I | R |
| Supplier security (TPRM) | I | R | **A** (requirements) | C | C | R |
| Security budget | **A** | R | R (business case) | C | I | I |

R = responsible, A = accountable, C = consulted, I = informed.

## Governance cadence

| Forum | Frequency | Chair | Purpose |
|---|---|---|---|
| Board cyber review | Quarterly | Board chair | Board pack, NIS2 oversight, accepted risks |
| COMEX risk committee | Monthly | CEO | Arbitration, budget, acceptances |
| Security steering (CIO / CISO / CTO) | Bi-weekly | CIO | Roadmap, KPIs, delivery blockers |
| Change advisory (security gate) | Weekly | CTO | Release decisions on risky changes |
| Crisis committee | On trigger | CEO | Major incident decisions and communication |

## Make or buy (CIO lens)

Build in-house what is differentiating or requires business context (risk governance, incident command, IAM governance). Buy what needs scale or 24/7 staffing (MDR, DDoS protection, backup immutability). See DEC-007 for the SOC decision.
