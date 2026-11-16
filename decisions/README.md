# Decision records

Each decision is stored in `data/decisions.json` and rendered into [`decision-journal.md`](decision-journal.md) with:

```
python tools/ciso.py decisions --output decisions/decision-journal.md
```

## Record template

| Field | Purpose |
|---|---|
| `context` | The situation and the evidence available at the time |
| `options` | Alternatives seriously considered (always at least two) |
| `decision` | What was decided, by whom |
| `rationale` | Why this option — trade-offs made explicit |
| `cost_eur` / `risks` | Resources committed and risks affected |
| `review_date` | When the decision must be re-examined |
| `outcome` | What actually happened — the journal learns from results |

A decision record protects the decision-maker too: it shows what was known, and what was traded off, when the call was made.
