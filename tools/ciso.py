#!/usr/bin/env python3
"""CISO / CIO governance toolkit.

Turns the machine-readable governance data in ``data/`` into decision support:
risk heatmaps, accepted-risk expiry, KPI status, ROSI, NIS2/DORA readiness,
third-party tiering, business-impact gaps, the decision journal and a full
board pack.

Usage (from the repository root):
    python tools/ciso.py validate
    python tools/ciso.py heatmap --view residual
    python tools/ciso.py risks
    python tools/ciso.py acceptances --as-of 2026-11-16
    python tools/ciso.py kpis
    python tools/ciso.py rosi
    python tools/ciso.py compliance
    python tools/ciso.py tprm
    python tools/ciso.py bia
    python tools/ciso.py decisions --output ciso-decision-journal.md
    python tools/ciso.py board-pack --as-of 2026-11-16 --output reports/board-pack.md
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
__version__ = "2.0.0"

DATA_ACCESS_WEIGHT = {"none": 1, "internal": 2, "personal": 3, "sensitive": 4}


# --------------------------------------------------------------------------------------------
# Loading & validation
# --------------------------------------------------------------------------------------------

def load(name: str, data_dir: Path = DATA):
    with (data_dir / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def load_all(data_dir: Path = DATA) -> Dict:
    return {
        "risks": load("risk_register.json", data_dir),
        "acceptances": load("risk_acceptance.json", data_dir),
        "decisions": load("decisions.json", data_dir),
        "kpis": load("kpis.json", data_dir),
        "investments": load("investments.json", data_dir),
        "compliance": load("compliance.json", data_dir),
        "vendors": load("third_parties.json", data_dir),
        "bia": load("bia.json", data_dir),
    }


def validate(d: Dict) -> List[str]:
    """Referential integrity checks: a governance dataset must be internally consistent."""
    errors: List[str] = []
    risk_ids = {r["id"] for r in d["risks"]}
    decision_ids = {x["id"] for x in d["decisions"]}
    if len(risk_ids) != len(d["risks"]):
        errors.append("Duplicate risk IDs")
    for r in d["risks"]:
        for view in ("inherent", "residual"):
            for axis in ("likelihood", "impact"):
                if not 1 <= r[view][axis] <= 5:
                    errors.append(f"{r['id']}: {view}.{axis} must be 1-5")
        if score(r, "residual") > score(r, "inherent"):
            errors.append(f"{r['id']}: residual risk higher than inherent risk")
        if not r.get("owner"):
            errors.append(f"{r['id']}: missing risk owner")
        errors += [f"{r['id']}: unknown decision {x}" for x in r.get("decisions", []) if x not in decision_ids]
    for a in d["acceptances"]:
        if a["risk_id"] not in risk_ids:
            errors.append(f"{a['id']}: unknown risk {a['risk_id']}")
        if date.fromisoformat(a["expires_on"]) <= date.fromisoformat(a["approved_on"]):
            errors.append(f"{a['id']}: expiry must follow approval")
        if not a.get("compensating_controls"):
            errors.append(f"{a['id']}: an accepted risk needs compensating controls")
    for x in d["decisions"]:
        errors += [f"{x['id']}: unknown risk {r}" for r in x.get("risks", []) if r not in risk_ids]
    for inv in d["investments"]:
        errors += [f"{inv['id']}: unknown risk {r}" for r in inv["risks"] if r not in risk_ids]
        if inv["aro_after"] > inv["aro_before"]:
            errors.append(f"{inv['id']}: ARO after investment cannot exceed ARO before")
    for k in d["kpis"]:
        if k["direction"] not in {"higher", "lower"}:
            errors.append(f"{k['id']}: direction must be 'higher' or 'lower'")
    return errors


# --------------------------------------------------------------------------------------------
# Risk
# --------------------------------------------------------------------------------------------

def score(risk: Dict, view: str = "residual") -> int:
    return risk[view]["likelihood"] * risk[view]["impact"]


def rating(value: int) -> str:
    if value >= 15:
        return "Critical"
    if value >= 10:
        return "High"
    if value >= 5:
        return "Medium"
    return "Low"


def heatmap(risks: List[Dict], view: str = "residual") -> str:
    """5x5 likelihood x impact matrix in Markdown."""
    cells: Dict[tuple, List[str]] = {}
    for r in risks:
        cells.setdefault((r[view]["likelihood"], r[view]["impact"]), []).append(r["id"])
    lines = [f"| Likelihood ↓ / Impact → | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
    for likelihood in range(5, 0, -1):
        row = [f"**{likelihood}**"]
        for impact in range(1, 6):
            ids = cells.get((likelihood, impact), [])
            marker = {"Critical": "🟥", "High": "🟧", "Medium": "🟨", "Low": "🟩"}[rating(likelihood * impact)]
            row.append(f"{marker} {' '.join(ids)}".strip())
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def risk_table(risks: List[Dict]) -> str:
    lines = ["| ID | Risk | Owner | Inherent | Residual | Reduction | Treatment |", "|---|---|---|---:|---:|---:|---|"]
    for r in sorted(risks, key=lambda r: -score(r)):
        inh, res = score(r, "inherent"), score(r)
        reduction = round(100 * (inh - res) / inh)
        lines.append(f"| {r['id']} | {r['name']} | {r['owner']} | {inh} {rating(inh)} | {res} {rating(res)} | "
                     f"{reduction}% | {r['treatment']} |")
    return "\n".join(lines)


def acceptance_status(acceptances: List[Dict], as_of: date, warn_days: int = 30) -> List[Dict]:
    out = []
    for a in acceptances:
        expires = date.fromisoformat(a["expires_on"])
        days = (expires - as_of).days
        status = "EXPIRED" if days < 0 else "EXPIRING" if days <= warn_days else "ACTIVE"
        out.append({**a, "days_left": days, "status": status})
    return sorted(out, key=lambda a: a["days_left"])


# --------------------------------------------------------------------------------------------
# KPIs, ROSI, compliance, third parties, BIA
# --------------------------------------------------------------------------------------------

def kpi_status(k: Dict) -> str:
    higher = k["direction"] == "higher"
    value, target, amber = k["value"], k["target"], k["amber"]
    if (value >= target) if higher else (value <= target):
        return "GREEN"
    if (value >= amber) if higher else (value <= amber):
        return "AMBER"
    return "RED"


def kpi_trend(k: Dict) -> str:
    if k.get("previous") is None or k["previous"] == k["value"]:
        return "→"
    improving = (k["value"] > k["previous"]) == (k["direction"] == "higher")
    return "↗ improving" if improving else "↘ worsening"


def rosi(inv: Dict) -> Dict:
    """Return on security investment: (ALE before − ALE after − cost) / cost."""
    ale_before = inv["sle_eur"] * inv["aro_before"]
    ale_after = inv["sle_eur"] * inv["aro_after"]
    reduction = ale_before - ale_after
    value = (reduction - inv["annual_cost_eur"]) / inv["annual_cost_eur"]
    return {**inv, "ale_before": round(ale_before), "ale_after": round(ale_after),
            "risk_reduction": round(reduction), "rosi_percent": round(100 * value, 1)}


def compliance_summary(compliance: Dict) -> List[Dict]:
    rows = []
    for framework, block in compliance.items():
        reqs = block["requirements"]
        rows.append({
            "framework": framework,
            "readiness": round(sum(r["score"] for r in reqs) / len(reqs), 1),
            "implemented": sum(r["status"] == "implemented" for r in reqs),
            "total": len(reqs),
            "weakest": sorted(reqs, key=lambda r: r["score"])[:3],
            "note": block.get("note", ""),
        })
    return rows


def vendor_tier(v: Dict, as_of: date) -> Dict:
    exposure = v["criticality"] * DATA_ACCESS_WEIGHT[v["data_access"]]
    tier = 1 if exposure >= 16 else 2 if exposure >= 9 else 3
    stale = v["last_assessed"] is None or (as_of - date.fromisoformat(v["last_assessed"])).days > 365
    issues = []
    if v["assessment_score"] is None:
        issues.append("never assessed")
    elif v["assessment_score"] < 60:
        issues.append(f"weak assessment ({v['assessment_score']}/100)")
    elif stale:
        issues.append("assessment older than 12 months")
    if not v["security_clauses"]:
        issues.append("no security clauses")
    if tier == 1 and not v["exit_plan"]:
        issues.append("no exit plan")
    return {**v, "exposure": exposure, "tier": tier, "issues": issues}


def bia_gaps(bia: List[Dict]) -> List[Dict]:
    rows = []
    for p in bia:
        rto_gap = p["rto_capability_h"] - p["rto_target_h"]
        rpo_gap = p["rpo_capability_h"] - p["rpo_target_h"]
        rows.append({**p, "rto_gap_h": rto_gap, "rpo_gap_h": rpo_gap, "compliant": rto_gap <= 0 and rpo_gap <= 0})
    # Non-compliant first, then the most time-critical processes (smallest RTO target).
    return sorted(rows, key=lambda p: (p["compliant"], p["rto_target_h"]))


# --------------------------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------------------------

def eur(value: float) -> str:
    return f"{value:,.0f} €".replace(",", " ")


def render_decisions(decisions: List[Dict]) -> str:
    lines = ["# CISO Decision Journal", "",
             "_Structured decision records: context, options, decision, rationale, cost, risks affected, "
             "review date and outcome. Generated from `data/decisions.json`._", "",
             "| ID | Date | Decision | Status |", "|---|---|---|---|"]
    lines += [f"| [{x['id']}](#{x['id'].lower()}) | {x['date']} | {x['title']} | {x['status']} |" for x in decisions]
    for x in decisions:
        lines += ["", f"## {x['id']}", "", f"### {x['title']}", "",
                  f"- **Date:** {x['date']} — **Decided by:** {x['decided_by']} — **Status:** {x['status']}",
                  f"- **Context:** {x['context']}",
                  "- **Options considered:** " + "; ".join(x["options"]),
                  f"- **Decision:** {x['decision']}",
                  f"- **Rationale:** {x['rationale']}",
                  f"- **Cost:** {eur(x['cost_eur']) if x['cost_eur'] else 'none'} — **Risks:** {', '.join(x['risks'])}",
                  f"- **Review date:** {x['review_date']}",
                  f"- **Outcome:** {x['outcome']}"]
    return "\n".join(lines) + "\n"


def render_board_pack(d: Dict, as_of: date, company: str = "Helios Docs (fictional B2B SaaS)") -> str:
    risks = d["risks"]
    residual_scores = [score(r) for r in risks]
    critical = [r for r in risks if rating(score(r)) == "Critical"]
    high = [r for r in risks if rating(score(r)) == "High"]
    inherent_total = sum(score(r, "inherent") for r in risks)
    reduction = round(100 * (inherent_total - sum(residual_scores)) / inherent_total)
    acceptances = acceptance_status(d["acceptances"], as_of)
    kpis = [{**k, "status": kpi_status(k), "trend": kpi_trend(k)} for k in d["kpis"]]
    reds = [k for k in kpis if k["status"] == "RED"]
    compliance = compliance_summary(d["compliance"])
    investments = sorted((rosi(i) for i in d["investments"]), key=lambda i: -i["rosi_percent"])
    vendors = sorted((vendor_tier(v, as_of) for v in d["vendors"]), key=lambda v: (v["tier"], -v["exposure"]))
    vendor_issues = [v for v in vendors if v["tier"] <= 2 and v["issues"]]
    gaps = [p for p in bia_gaps(d["bia"]) if not p["compliant"]]
    pending = [x for x in d["decisions"] if x["status"] in {"In progress", "Planned"}]

    posture = "Elevated" if critical else "Moderate" if high else "Controlled"
    lines = [
        f"# Board Security & Resilience Pack — {as_of.isoformat()}", "",
        f"_{company}. Generated by `tools/ciso.py` v{__version__} from `data/`. Synthetic portfolio data._", "",
        "## 1. Headline", "",
        f"- **Overall cyber risk posture:** {posture} — {len(critical)} critical and {len(high)} high residual risks "
        f"out of {len(risks)}; controls reduce aggregate exposure by **{reduction}%**.",
        f"- **KPIs:** {sum(k['status'] == 'GREEN' for k in kpis)} green, {sum(k['status'] == 'AMBER' for k in kpis)} amber, "
        f"**{len(reds)} red**.",
        "- **Regulatory readiness:** " + ", ".join(f"{c['framework']} {c['readiness']}%" for c in compliance) + ".",
        f"- **Accepted risks:** {sum(a['status'] == 'EXPIRED' for a in acceptances)} expired, "
        f"{sum(a['status'] == 'EXPIRING' for a in acceptances)} expiring within 30 days.",
        f"- **Resilience:** {len(gaps)} business process(es) cannot meet their recovery objectives today.", "",
        "## 2. Residual risk heatmap", "", heatmap(risks, "residual"), "",
        "## 3. Risk register (sorted by residual risk)", "", risk_table(risks), "",
        "## 4. Key performance & risk indicators", "",
        "| KPI | Value | Target | Status | Trend |", "|---|---:|---:|---|---|",
    ]
    for k in kpis:
        icon = {"GREEN": "🟢", "AMBER": "🟠", "RED": "🔴"}[k["status"]]
        lines.append(f"| {k['name']} | {k['value']}{k['unit']} | {k['target']}{k['unit']} | {icon} {k['status']} | {k['trend']} |")
    lines += ["", "## 5. Regulatory readiness", ""]
    for c in compliance:
        lines += [f"**{c['framework']} — {c['readiness']}% ({c['implemented']}/{c['total']} requirements fully implemented).** "
                  f"{c['note']}", "", "Weakest areas: " + "; ".join(f"{w['ref']} {w['title']} ({w['score']}%)" for w in c["weakest"]), ""]
    lines += ["## 6. Accepted risks", "", "| ID | Risk | Description | Owner | Expires | Status |", "|---|---|---|---|---|---|"]
    for a in acceptances:
        lines.append(f"| {a['id']} | {a['risk_id']} | {a['description']} | {a['risk_owner']} | {a['expires_on']} | {a['status']} |")
    lines += ["", "## 7. Security investments — return on security investment (ROSI)", "",
              "| Investment | Annual cost | ALE before | ALE after | Risk reduction | ROSI |", "|---|---:|---:|---:|---:|---:|"]
    for i in investments:
        lines.append(f"| {i['name']} | {eur(i['annual_cost_eur'])} | {eur(i['ale_before'])} | {eur(i['ale_after'])} | "
                     f"{eur(i['risk_reduction'])} | {i['rosi_percent']}% |")
    lines += ["", "_ALE = single loss expectancy × annual rate of occurrence. Estimates are order-of-magnitude, for prioritisation._", "",
              "## 8. Third-party risk", "", "| Supplier | Tier | Criticality | Data | Issues |", "|---|---:|---:|---|---|"]
    for v in vendor_issues:
        lines.append(f"| {v['name']} | {v['tier']} | {v['criticality']} | {v['data_access']} | {', '.join(v['issues'])} |")
    lines += ["", "## 9. Business continuity (BIA)", "", "| Process | Owner | RTO target / capability | RPO target / capability |",
              "|---|---|---|---|"]
    for p in gaps:
        lines.append(f"| {p['process']} | {p['owner']} | {p['rto_target_h']}h / **{p['rto_capability_h']}h** | "
                     f"{p['rpo_target_h']}h / **{p['rpo_capability_h']}h** |")
    lines += ["", "## 10. Decisions in flight", ""]
    lines += [f"- **{x['id']} — {x['title']}** ({x['status']}, review {x['review_date']}): {x['outcome']}" for x in pending]

    asks = []
    for a in acceptances:
        if a["status"] == "EXPIRED":
            asks.append(f"Close or renew expired acceptance {a['id']} ({a['description']}) — accepted risk must stay time-bound.")
        elif a["status"] == "EXPIRING":
            asks.append(f"Confirm the plan to retire acceptance {a['id']} ({a['description']}) before {a['expires_on']}.")
    if investments and investments[0]["rosi_percent"] > 0:
        best = [i for i in investments if i["rosi_percent"] > 0 and not i["decision"]]
        if best:
            asks.append(f"Approve '{best[0]['name']}' ({eur(best[0]['annual_cost_eur'])}/year, ROSI {best[0]['rosi_percent']}%).")
    if gaps:
        asks.append("Confirm funding to close recovery gaps on: " + ", ".join(p["process"] for p in gaps)
                    + " (SaaS platform gap addressed by DEC-008).")
    if vendor_issues:
        asks.append(f"Mandate security assessments and contract clauses for {len(vendor_issues)} tier-1/2 supplier(s).")
    for k in reds[:2]:
        asks.append(f"Sponsor corrective action on red KPI '{k['name']}' ({k['value']}{k['unit']} vs {k['target']}{k['unit']}).")
    lines += ["", "## 11. Decisions requested from the board", ""] + [f"{n}. {a}" for n, a in enumerate(asks, 1)]
    lines += ["", "---", "_A CISO does not eliminate risk: the role is to make it visible, measurable and consciously accepted._", ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------

def _out(content: str, output: Optional[str]) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"[+] written to {output}", file=sys.stderr)
    else:
        print(content)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="CISO / CIO governance toolkit")
    parser.add_argument("--data-dir", default=str(DATA), help="Directory containing the JSON data files")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Reference date (YYYY-MM-DD)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Check referential integrity of the data")
    hm = sub.add_parser("heatmap", help="5x5 risk heatmap")
    hm.add_argument("--view", choices=["inherent", "residual"], default="residual")
    sub.add_parser("risks", help="Risk register with inherent vs residual scores")
    sub.add_parser("acceptances", help="Accepted risks and their expiry status")
    sub.add_parser("kpis", help="KPI / KRI status (RAG)")
    sub.add_parser("rosi", help="Return on security investment ranking")
    sub.add_parser("compliance", help="NIS2 / DORA readiness")
    sub.add_parser("tprm", help="Third-party risk tiering")
    sub.add_parser("bia", help="Business impact analysis gaps (RTO / RPO)")
    for name in ("decisions", "board-pack"):
        p = sub.add_parser(name, help="Generate the decision journal" if name == "decisions" else "Generate the board pack")
        p.add_argument("--output")
    args = parser.parse_args(argv)

    d = load_all(Path(args.data_dir))
    as_of = date.fromisoformat(args.as_of)

    if args.command == "validate":
        errors = validate(d)
        print("\n".join(f"[!] {e}" for e in errors) if errors else "[+] Data is consistent.")
        return 1 if errors else 0
    if args.command == "heatmap":
        print(heatmap(d["risks"], args.view))
    elif args.command == "risks":
        print(risk_table(d["risks"]))
    elif args.command == "acceptances":
        for a in acceptance_status(d["acceptances"], as_of):
            print(f"{a['status']:<9} {a['id']} ({a['risk_id']}) {a['description']} — expires {a['expires_on']} ({a['days_left']} days)")
    elif args.command == "kpis":
        for k in d["kpis"]:
            print(f"{kpi_status(k):<6} {k['name']}: {k['value']}{k['unit']} (target {k['target']}{k['unit']}) {kpi_trend(k)}")
    elif args.command == "rosi":
        for i in sorted((rosi(x) for x in d["investments"]), key=lambda i: -i["rosi_percent"]):
            print(f"{i['rosi_percent']:>7}%  {i['name']} — cost {eur(i['annual_cost_eur'])}, risk reduction {eur(i['risk_reduction'])}")
    elif args.command == "compliance":
        for c in compliance_summary(d["compliance"]):
            print(f"{c['framework']}: {c['readiness']}% ready ({c['implemented']}/{c['total']} implemented)")
            for w in c["weakest"]:
                print(f"   gap: {w['ref']} {w['title']} ({w['score']}%) — owner {w['owner']}")
    elif args.command == "tprm":
        for v in sorted((vendor_tier(x, as_of) for x in d["vendors"]), key=lambda v: (v["tier"], -v["exposure"])):
            print(f"Tier {v['tier']}  {v['name']:<34} {', '.join(v['issues']) or 'OK'}")
    elif args.command == "bia":
        for p in bia_gaps(d["bia"]):
            flag = "OK " if p["compliant"] else "GAP"
            print(f"{flag} {p['process']:<34} RTO {p['rto_capability_h']}h/{p['rto_target_h']}h  RPO {p['rpo_capability_h']}h/{p['rpo_target_h']}h")
    elif args.command == "decisions":
        _out(render_decisions(d["decisions"]), args.output)
    elif args.command == "board-pack":
        _out(render_board_pack(d, as_of), args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
