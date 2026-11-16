# Changelog

## 2.0.0
- Repository reorganised into governance / decisions / risk / compliance / incidents / board / data / tools / reports.
- Data model: 10 risks with inherent and residual scores, time-bound acceptances, 8 structured decisions, KPIs/KRIs, investments (ALE/ROSI), NIS2 and DORA requirements, suppliers, BIA.
- `tools/ciso.py`: validate, heatmap, risks, acceptances, kpis, rosi, compliance, tprm, bia, decisions, board-pack.
- New documents: CISO–CIO operating model with RACI and governance cadence, risk methodology, acceptance policy, enriched incident case with the NIS2 regulatory clock.
- Generated board pack and decision journal; pytest suite and CI (data integrity check).
- v1 scripts kept as compatibility wrappers (and the v1 relative-path bug is fixed).
