
import json

def score_risk(likelihood, impact):
    return likelihood * impact

with open('../data/risk_register.json') as f:
    risks = json.load(f)

print("=== Risk Scoring ===")
for r in risks:
    score = score_risk(r["likelihood"], r["impact"])
    print(f'{r["id"]}: {r["name"]} -> score {score}')
