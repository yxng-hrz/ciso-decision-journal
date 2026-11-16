import json
import shutil
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ciso  # noqa: E402

AS_OF = date(2026, 11, 16)


@pytest.fixture()
def data():
    return ciso.load_all()


def test_repository_data_is_consistent(data):
    assert ciso.validate(data) == []


def test_validation_catches_broken_references(tmp_path, data):
    shutil.copytree(ciso.DATA, tmp_path / "data")
    risks = json.loads((tmp_path / "data" / "risk_register.json").read_text())
    risks[0]["residual"]["likelihood"] = 5
    risks[0]["decisions"].append("DEC-999")
    (tmp_path / "data" / "risk_register.json").write_text(json.dumps(risks))
    errors = ciso.validate(ciso.load_all(tmp_path / "data"))
    assert any("residual risk higher" in e for e in errors)
    assert any("DEC-999" in e for e in errors)
    assert ciso.main(["--data-dir", str(tmp_path / "data"), "validate"]) == 1


def test_scoring_and_ratings():
    assert [ciso.rating(v) for v in (25, 15, 12, 5, 4)] == ["Critical", "Critical", "High", "Medium", "Low"]
    risk = {"inherent": {"likelihood": 4, "impact": 5}, "residual": {"likelihood": 2, "impact": 5}}
    assert ciso.score(risk, "inherent") == 20 and ciso.score(risk) == 10


def test_heatmap_places_every_risk(data):
    grid = ciso.heatmap(data["risks"])
    assert all(r["id"] in grid for r in data["risks"])


def test_acceptance_expiry(data):
    statuses = {a["id"]: a["status"] for a in ciso.acceptance_status(data["acceptances"], AS_OF)}
    assert statuses == {"A1": "EXPIRED", "A2": "EXPIRING", "A3": "ACTIVE"}


def test_kpi_status_handles_both_directions():
    higher = {"value": 92, "target": 95, "amber": 90, "direction": "higher", "previous": 80}
    lower = {"value": 30, "target": 24, "amber": 48, "direction": "lower", "previous": 50}
    assert ciso.kpi_status(higher) == "AMBER" and ciso.kpi_trend(higher).startswith("↗")
    assert ciso.kpi_status(lower) == "AMBER" and ciso.kpi_trend(lower).startswith("↗")
    assert ciso.kpi_status({**lower, "value": 60}) == "RED"


def test_rosi_formula():
    result = ciso.rosi({"annual_cost_eur": 100, "sle_eur": 1000, "aro_before": 0.5, "aro_after": 0.2})
    assert result["ale_before"] == 500 and result["ale_after"] == 200
    assert result["rosi_percent"] == 200.0


def test_vendor_tiering(data):
    vendors = {v["name"]: ciso.vendor_tier(v, AS_OF) for v in data["vendors"]}
    contractor = vendors["Offshore development contractor"]
    assert contractor["tier"] == 1 and "no security clauses" in contractor["issues"]
    assert vendors["Marketing automation tool"]["tier"] == 3


def test_bia_gaps_put_saas_first(data):
    gaps = [p for p in ciso.bia_gaps(data["bia"]) if not p["compliant"]]
    assert gaps[0]["process"].startswith("SaaS platform")


def test_board_pack_contains_every_section(data):
    pack = ciso.render_board_pack(data, AS_OF)
    for heading in ("Headline", "heatmap", "KPI", "Regulatory readiness", "ROSI", "Third-party", "BIA",
                    "Decisions requested"):
        assert heading.lower() in pack.lower()
    assert "Close or renew expired acceptance A1" in pack


def test_decision_journal_renders_all_records(data):
    journal = ciso.render_decisions(data["decisions"])
    assert all(x["id"] in journal for x in data["decisions"])
