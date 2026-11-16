# Risk Acceptance Policy & Register

Accepting a risk is a **business decision**, not a security failure — provided it is explicit, owned and temporary.

## Rules

1. Only an executive **risk owner** can accept a risk; the CISO gives a written opinion.
2. Every acceptance lists **compensating controls** and a **justification**.
3. Every acceptance has an **expiry date** (12 months maximum). On expiry the risk is renewed with fresh evidence or treated — never silently extended.
4. High and critical residual risks are accepted at **COMEX** level; concentration and existential risks at **board** level.
5. Expired or expiring acceptances appear automatically in the board pack (`tools/ciso.py acceptances`).

## Register (source: `data/risk_acceptance.json`)

| ID | Risk | Description | Approved by | Expires | Status on 2026-11-16 |
|---|---|---|---|---|---|
| A1 | R9 | No in-house SIEM platform | Executive Committee | 2026-11-01 | 🔴 Expired — to be closed by the MDR go-live (DEC-007) |
| A2 | R9 | No 24/7 internal SOC | Executive Committee | 2026-12-15 | 🟠 Expiring — bridge until MDR onboarding |
| A3 | R3 | Single cloud provider | Board | 2027-03-01 | 🟢 Active — exit plan documented |
