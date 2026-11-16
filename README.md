# CISO Decision Journal — CISO & CIO Governance Portfolio

**An end-to-end simulation of how a CISO / CIO governs cyber risk in a growing SaaS company — with the decisions, the trade-offs, the evidence and the tooling that turns governance data into a board pack.**

> A CISO does not eliminate risk.
> A CISO makes risk visible, understandable and consciously accepted.

This repository is not a collection of policies. It shows the **judgment** behind security leadership: what was decided, which options were rejected, what it cost, which risk was accepted, by whom and until when — and what actually happened afterwards.

## What it demonstrates

| Leadership skill | Where |
|---|---|
| Risk governance (inherent vs residual, owners, treatment) | `risk/`, `data/risk_register.json` |
| Decision-making under constraints, with outcomes | `decisions/decision-journal.md` (8 records) |
| Time-bound risk acceptance | `risk/risk-acceptance-policy.md`, `data/risk_acceptance.json` |
| Board communication | `board/`, `reports/board-pack.md` |
| CISO / CIO operating model, RACI, make-or-buy | `governance/operating-model.md` |
| NIS2 and DORA readiness | `compliance/nis2-dora-alignment.md` |
| Crisis management with the regulatory clock | `incidents/` |
| Security economics (ALE, ROSI) | `data/investments.json` |
| Third-party risk and business continuity (BIA, RTO/RPO) | `data/third_parties.json`, `data/bia.json` |

## Repository structure

```text
governance/   company context, CISO positioning, CISO-CIO operating model (RACI), roadmap
decisions/    structured decision records (context, options, rationale, cost, outcome)
risk/         methodology, acceptance policy and register
compliance/   NIS2 Art. 20/21/23 and DORA (ICT third-party provider) alignment
incidents/    ransomware case with NIS2 24h/72h/1-month timeline, post-incident report
board/        annual CISO letter, COMEX one-pager
data/         machine-readable governance data (single source of truth)
tools/        ciso.py — governance toolkit (validation, heatmap, KPIs, ROSI, board pack)
reports/      generated board pack
tests/        pytest suite for the toolkit
```

## The toolkit

Everything in the board pack is computed from `data/` — no number is typed twice.

```bash
python tools/ciso.py validate                 # referential integrity (risks ↔ decisions ↔ acceptances)
python tools/ciso.py heatmap --view residual  # 5x5 likelihood x impact matrix
python tools/ciso.py risks                    # inherent vs residual, reduction per risk
python tools/ciso.py acceptances              # expired / expiring accepted risks
python tools/ciso.py kpis                     # RAG status and trend of 9 KPIs/KRIs
python tools/ciso.py rosi                     # return on security investment ranking
python tools/ciso.py compliance               # NIS2 / DORA readiness and weakest areas
python tools/ciso.py tprm                     # supplier tiering and contract gaps
python tools/ciso.py bia                      # processes that cannot meet RTO / RPO
python tools/ciso.py decisions --output decisions/decision-journal.md
python tools/ciso.py board-pack --output reports/board-pack.md
```

Use `--as-of YYYY-MM-DD` to reproduce a report at a given date. No dependency beyond the Python standard library (3.9+); `pytest` for tests.

### What the board pack contains

Headline posture, residual heatmap, risk register, KPI dashboard, NIS2/DORA readiness, accepted risks with expiry, ROSI of proposed investments, supplier issues, recovery gaps, decisions in flight and **decisions requested from the board** — generated from the data, so an expired acceptance or a red KPI automatically becomes a board ask.

## Highlights of the scenario

- **8 decisions**, including a delayed release, a declined deal, a "prevention before SIEM" budget call later superseded by an MDR make-or-buy decision, and a second-region investment driven by the BIA.
- A **ransomware incident** handled within NIS2 and GDPR deadlines, without paying.
- One security investment shows a **negative ROSI** (TPRM platform): the right answer is a process, not a tool — the model is there to challenge spending, not to justify it.

## Disclaimer

The company, figures and incidents are fictional and built for a portfolio. Regulatory mappings are indicative and not legal advice.

## License

MIT
