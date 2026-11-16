# Enterprise Risk Methodology

## Scales

| Score | Likelihood (12 months) | Impact |
|---|---|---|
| 1 | Rare (< 5%) | Negligible: no customer impact, < €10k |
| 2 | Unlikely (5–20%) | Minor: limited internal disruption, < €100k |
| 3 | Possible (20–50%) | Moderate: customer-visible incident, < €500k |
| 4 | Likely (50–80%) | Major: multi-day outage or personal data breach, < €2M |
| 5 | Almost certain (> 80%) | Severe: existential, regulatory sanction, > €2M |

Risk = likelihood × impact. **Critical ≥ 15**, High 10–14, Medium 5–9, Low < 5.

## Inherent vs residual

Each risk in `data/risk_register.json` carries an **inherent** score (no controls) and a **residual** score (current controls). The gap shows what the security programme actually buys; a residual score higher than the inherent one is rejected by `tools/ciso.py validate`.

## Treatment options

Reduce (controls), transfer (insurance, contract), avoid (stop the activity) or **accept**. Acceptance follows `risk-acceptance-policy.md`.

## Critical assets

| Asset | Description | Impact if compromised |
|---|---|---|
| Customer documents | Contracts, HR and financial records of customers | Severe |
| SaaS platform | Core revenue service | Severe |
| Cloud control plane & IAM | Administrative access to everything | Severe |
| Source code & CI/CD | Integrity of every release | Major |
| Brand and customer trust | Commercial pipeline | Major |
| Key personnel | DevOps and senior engineers | Moderate |

## Current picture

Run `python tools/ciso.py heatmap` and `python tools/ciso.py risks`, or read sections 2–3 of [`reports/board-pack.md`](../reports/board-pack.md).
