"""Checks the tools against sample-data/answer_key.csv. Run: pytest tests/"""

import csv
from pathlib import Path

from bw_triage import tools

ANSWER_KEY = Path(__file__).resolve().parents[2] / "sample-data" / "answer_key.csv"


def _key():
    with open(ANSWER_KEY, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_chains_needing_attention_match_answer_key():
    result = tools.get_overnight_status()
    expected = [r for r in _key() if r["order"] != "-"]
    got = result["chains_needing_attention"]
    assert [c["chain_id"] for c in got] == [r["chain_id"] for r in expected]
    for c, r in zip(got, expected):
        assert c["status"] == r["expected_status"], c["chain_id"]
        assert len(c["affected_reports"]) == int(r["affected_reports"]), c["chain_id"]


def test_successful_chains():
    result = tools.get_overnight_status()
    expected = {r["chain_id"] for r in _key() if r["order"] == "-"}
    assert {c["chain_id"] for c in result["other_chains"]} == expected


def test_summary_line():
    assert tools.get_overnight_status()["summary_line"] == (
        "8 chains need attention. 15 reports are showing stale data."
    )


def test_runbook_matching_and_escalation():
    chains = {c["chain_id"]: c for c in tools.get_overnight_status()["chains_needing_attention"]}
    assert chains["ZPC_SD_DAILY"]["escalate_to"] == "Ravi Menon"
    assert chains["ZPC_SD_DAILY"]["standard_fix"].endswith("Escalate to Ravi Menon")
    assert chains["ZPC_CO_MARGIN"]["in_runbook"] is False
    assert chains["ZPC_CO_MARGIN"]["standard_fix"] == "not in the runbook"
    assert chains["ZPC_PUR_PO"]["owner"] == "Basis team"
    assert "Grace Liu" in chains["ZPC_HR_HEADCOUNT"]["owner"]
    assert "Do not change the permitted characters setting" in chains["ZPC_HR_HEADCOUNT"]["standard_fix"]
    for cid in ("ZPC_MM_STOCK", "ZPC_PUR_PO", "ZPC_HR_HEADCOUNT", "ZPC_CO_MARGIN"):
        assert "escalate_to" not in chains[cid]


def test_late_chains():
    chains = {c["chain_id"]: c for c in tools.get_overnight_status()["chains_needing_attention"]}
    assert chains["ZPC_FI_GL"]["minutes_late"] == 42
    assert chains["ZPC_FI_GL"]["still_running"] is False
    assert chains["ZPC_SCM_FCST"]["minutes_late"] == 30
    assert chains["ZPC_SCM_FCST"]["still_running"] is True


def test_stale_reports_count_kpi_cockpit_once():
    result = tools.get_stale_reports()
    assert result["stale_report_count"] == 15
    assert result["stale_reports"].count("Executive KPI cockpit") == 1
    assert [c["chain_id"] for c in result["late_chains_now_finished"]] == ["ZPC_FI_GL"]


def test_business_update_for_sales():
    facts = tools.get_business_update_facts("sales")
    assert facts["user_group"] == "Sales users"
    assert facts["not_updated"] == [
        "Daily sales dashboard", "Sales by region", "Sales vs. target",
        "Weekly sales email", "Executive KPI cockpit",
    ]
    assert facts["may_be_incomplete"] == ["Billing overview", "Revenue by product"]
    assert "Order backlog" not in facts["not_updated"] + facts["may_be_incomplete"]


def test_unknown_group_and_chain():
    assert "known_user_groups" in tools.get_business_update_facts("marketing")
    assert "known_chains" in tools.get_chain_details("payroll")


def test_chain_details_by_name():
    d = tools.get_chain_details("material master data")
    assert d["latest_run"]["status"] == "SUCCESS"
    assert d["latest_run"]["finished_at"] == "01:10"
    d = tools.get_chain_details("inventory snapshot")
    assert "No SID found" in d["latest_run"]["error_message"]
