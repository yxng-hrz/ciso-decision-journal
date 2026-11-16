# CISO Decision Journal

_Structured decision records: context, options, decision, rationale, cost, risks affected, review date and outcome. Generated from `data/decisions.json`._

| ID | Date | Decision | Status |
|---|---|---|---|
| [DEC-001](#dec-001) | 2025-01-15 | Company-wide MFA, including executives and contractors | Implemented |
| [DEC-002](#dec-002) | 2025-04-03 | Delay a feature release by two weeks for a security review | Implemented |
| [DEC-003](#dec-003) | 2025-06-20 | Decline unrealistic contractual security guarantees | Implemented |
| [DEC-004](#dec-004) | 2025-09-10 | Prioritise prevention over a SIEM in the 2026 budget | Superseded by DEC-007 |
| [DEC-005](#dec-005) | 2026-02-12 | Incident disclosure strategy after the ransomware case | Implemented |
| [DEC-006](#dec-006) | 2026-03-05 | Launch a NIS2 compliance programme with board oversight | In progress |
| [DEC-007](#dec-007) | 2026-06-15 | Buy managed detection & response (MDR) rather than build a SOC | In progress |
| [DEC-008](#dec-008) | 2026-09-22 | Fund a warm standby in a second cloud region | Planned |

## DEC-001

### Company-wide MFA, including executives and contractors

- **Date:** 2025-01-15 — **Decided by:** CISO, endorsed by COMEX — **Status:** Implemented
- **Context:** Account compromise is the main initial-access vector; 18% of staff had MFA.
- **Options considered:** MFA for admins only; Company-wide MFA; Passwordless roadmap first
- **Decision:** Company-wide MFA within 60 days, phishing-resistant for administrators.
- **Rationale:** Highest risk reduction per euro; prerequisite for any zero-trust step.
- **Cost:** 12 000 € — **Risks:** R1, R2
- **Review date:** 2026-01-15
- **Outcome:** MFA coverage 98%; no account takeover since rollout.

## DEC-002

### Delay a feature release by two weeks for a security review

- **Date:** 2025-04-03 — **Decided by:** CISO with CPO, arbitrated by CEO — **Status:** Implemented
- **Context:** Pentest found an authorisation flaw exposing tenant data, two days before launch.
- **Options considered:** Ship and hotfix; Ship behind feature flag; Delay two weeks
- **Decision:** Delay the release by two weeks and fix the flaw.
- **Rationale:** Cross-tenant exposure would breach customer contracts and GDPR; reputational impact outweighs two weeks of delay.
- **Cost:** none — **Risks:** R7, R4
- **Review date:** 2025-10-03
- **Outcome:** Release shipped without incident; security review now a release gate.

## DEC-003

### Decline unrealistic contractual security guarantees

- **Date:** 2025-06-20 — **Decided by:** CEO on CISO and legal advice — **Status:** Implemented
- **Context:** A large prospect required a 'zero breach' guarantee with uncapped liability.
- **Options considered:** Accept as is; Negotiate standard security annex; Decline the deal
- **Decision:** Propose a standard security annex; decline when the prospect refused.
- **Rationale:** An unmeasurable guarantee creates unbounded legal exposure; credibility depends on promises we can keep.
- **Cost:** none — **Risks:** R4
- **Review date:** 2026-06-20
- **Outcome:** Standard security annex created and reused in 14 contracts.

## DEC-004

### Prioritise prevention over a SIEM in the 2026 budget

- **Date:** 2025-09-10 — **Decided by:** COMEX — **Status:** Superseded by DEC-007
- **Context:** Budget allowed either a SIEM project or prevention controls (EDR, backups, MFA).
- **Options considered:** Build a SIEM; Prevention first and accept detection gap; Split the budget
- **Decision:** Fund prevention first; formally accept the detection gap for 12 months (A1).
- **Rationale:** A SIEM without analysts adds cost but little detection; prevention reduces likelihood immediately.
- **Cost:** 95 000 € — **Risks:** R1, R9
- **Review date:** 2026-09-10
- **Outcome:** EDR and immutable backups deployed; acceptance A1 reached expiry and must now be closed by DEC-007.

## DEC-005

### Incident disclosure strategy after the ransomware case

- **Date:** 2026-02-12 — **Decided by:** Crisis committee chaired by CEO — **Status:** Implemented
- **Context:** Ransomware encrypted part of production (see incident case); customers and regulator to be informed.
- **Options considered:** Minimal disclosure; Transparent disclosure within regulatory deadlines; Delay until full investigation
- **Decision:** Transparent, staged disclosure aligned with NIS2 timelines (24h / 72h / 1 month) and GDPR 72h.
- **Rationale:** Trust is the product; early factual communication limits reputational damage.
- **Cost:** none — **Risks:** R1, R4
- **Review date:** 2026-08-12
- **Outcome:** No customer churn attributed to the incident; regulator acknowledged timely notification.

## DEC-006

### Launch a NIS2 compliance programme with board oversight

- **Date:** 2026-03-05 — **Decided by:** Board — **Status:** In progress
- **Context:** The company is likely in NIS2 scope as an important entity; management bodies must approve and oversee measures.
- **Options considered:** Wait for national transposition details; Launch programme now
- **Decision:** Launch a 12-month programme, board training, quarterly reporting to the board.
- **Rationale:** Management liability and customer due-diligence pressure make waiting more costly than acting.
- **Cost:** 60 000 € — **Risks:** R4
- **Review date:** 2026-12-05
- **Outcome:** Readiness tracked in compliance/nis2-dora-alignment.md.

## DEC-007

### Buy managed detection & response (MDR) rather than build a SOC

- **Date:** 2026-06-15 — **Decided by:** CISO and CIO, approved by COMEX — **Status:** In progress
- **Context:** Detection gap (R9) persisted after DEC-004; hiring 5 analysts for 24/7 coverage is not realistic.
- **Options considered:** Build internal 24/7 SOC; Buy MDR service; Status quo
- **Decision:** Contract an MDR provider with 24/7 response; keep incident command in-house.
- **Rationale:** Make-or-buy: MDR delivers 24/7 coverage at about one third of an internal SOC cost, faster.
- **Cost:** 85 000 € — **Risks:** R1, R9
- **Review date:** 2027-01-31
- **Outcome:** Contract signed; onboarding due January 2027. Acceptance A2 bridges the gap until then.

## DEC-008

### Fund a warm standby in a second cloud region

- **Date:** 2026-09-22 — **Decided by:** CIO, approved by COMEX — **Status:** Planned
- **Context:** BIA shows the SaaS platform RTO (4h) is not achievable from backups alone (12h).
- **Options considered:** Accept current RTO; Warm standby in second region; Active-active multi-region
- **Decision:** Warm standby in a second EU region; active-active rejected as disproportionate.
- **Rationale:** Closes the RTO gap for the core revenue service at 40% of the active-active cost.
- **Cost:** 120 000 € — **Risks:** R3
- **Review date:** 2027-06-30
- **Outcome:** Pending.
