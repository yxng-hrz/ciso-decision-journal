
import json

with open('../data/risk_register.json') as f:
    risks = json.load(f)

critical = [r for r in risks if r["likelihood"] * r["impact"] >= 16]

print("=== COMEX SECURITY DASHBOARD ===")
print(f"Total risks: {len(risks)}")
print(f"Critical risks: {len(critical)}")

for r in critical:
    print(f'- {r["id"]}: {r["name"]} (Owner: {r["owner"]})')
