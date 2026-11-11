"""Read-only tools for the BW Load Triage agent.

The tools do the exact work (classifying runs, matching the runbook,
counting reports) in code, so the model only explains the results.

They read the sample files in ./data. To connect a real SAP BW system,
replace the three _load_* functions with calls to your read-only data
source (for example an OData service over the process chain logs).
Keep the return shapes the same and the agents need no changes.
"""

from __future__ import annotations

import csv
import os
import re
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.environ.get("BW_DATA_DIR", Path(__file__).parent / "data"))
TIME_FMT = "%Y-%m-%d %H:%M"
STATUS_ORDER = {"FAILED": 0, "LATE": 1, "WARNING": 2}


# --------------------------------------------------------------------------
# Data access. Replace these with your real source.
# --------------------------------------------------------------------------

def _read_csv(name: str) -> list[dict]:
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _load_run_log() -> list[dict]:
    return _read_csv("chain_run_log.csv")


def _load_schedule() -> dict[str, dict]:
    return {r["chain_id"]: r for r in _read_csv("chain_schedule.csv")}


def _load_impact_map() -> list[dict]:
    return _read_csv("report_impact_map.csv")


def _load_runbook() -> dict:
    """Parse the runbook: known errors, escalation contact, data owners, export time."""
    text = (DATA_DIR / "runbook.md").read_text(encoding="utf-8")

    errors = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("## Known errors"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if in_table and line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells[0] == "Error":
                continue
            errors.append({
                "error": cells[0],
                "patterns": re.findall(r'"([^"]+)"', cells[1]),
                "likely_cause": cells[2],
                "standard_fix": cells[3],
                "owner": cells[4],
            })

    esc = re.search(r"escalate to the [^,]+, \*\*([^*]+)\*\*", text)
    owners = {}
    owner_section = text.split("## Data owners by area", 1)[-1]
    for m in re.finditer(r"^- (.+?): (.+)$", owner_section, re.M):
        for area in re.split(r",\s*|\s+and\s+", m.group(1)):
            owners[area.strip().lower()] = m.group(2).strip()

    exported = re.search(r"exported at \*\*(\d{2}:\d{2}) on ([A-Za-z]+ \d{1,2}, \d{4})\*\*", text)
    exported_at = None
    if exported:
        exported_at = datetime.strptime(f"{exported.group(2)} {exported.group(1)}", "%B %d, %Y %H:%M")

    return {
        "errors": errors,
        "escalation_contact": esc.group(1) if esc else None,
        "data_owners": owners,
        "exported_at": exported_at,
    }


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _ts(value: str):
    return datetime.strptime(value, TIME_FMT) if value else None


def _export_time(runbook: dict, log: list[dict]) -> datetime:
    override = os.environ.get("BW_LOG_EXPORTED_AT")
    if override:
        return datetime.strptime(override, TIME_FMT)
    if runbook["exported_at"]:
        return runbook["exported_at"]
    return datetime.now()


def _runs_by_date(log: list[dict]) -> dict[str, dict[str, list[dict]]]:
    """{run_date: {chain_id: [steps]}}, a run's date is the date its first step started."""
    by_date: dict[str, dict[str, list[dict]]] = {}
    last_date: dict[str, str] = {}
    for row in log:  # the log is in run order
        chain = row["chain_id"]
        if row["start_time"]:
            last_date[chain] = row["start_time"][:10]
        date = last_date.get(chain)  # a step that never started belongs to its chain's current run
        if date:
            by_date.setdefault(date, {}).setdefault(chain, []).append(row)
    return by_date


def _match_runbook(error_message: str, runbook: dict) -> dict | None:
    for entry in runbook["errors"]:
        if entry["patterns"] and all(p.lower() in error_message.lower() for p in entry["patterns"]):
            return entry
    return None


def _area_owner(area: str, runbook: dict) -> str | None:
    return runbook["data_owners"].get(area.strip().lower())


def _reports_for(chain_id: str, impact: list[dict]) -> list[dict]:
    return [r for r in impact if r["chain_id"] == chain_id]


def _classify(chain_id: str, steps: list[dict], schedule: dict, export_at: datetime) -> dict:
    sched = schedule.get(chain_id, {})
    run_date = min(s["start_time"] for s in steps if s["start_time"])[:10]
    expected = _ts(f"{run_date} {sched['expected_finish_time']}") if sched else None
    failed = next((s for s in steps if s["status"] == "FAILED"), None)
    running = any(s["status"] == "RUNNING" for s in steps)
    warning = next((s for s in steps if s["status"] == "WARNING"), None)
    ends = [_ts(s["end_time"]) for s in steps if s["end_time"]]
    finished_at = None if running else (max(ends) if ends else None)

    result = {
        "chain_id": chain_id,
        "chain_description": steps[0]["chain_description"],
        "area": sched.get("area"),
        "run_date": run_date,
        "expected_finish": sched.get("expected_finish_time"),
        "finished_at": finished_at.strftime("%H:%M") if finished_at else None,
        "still_running": running,
    }
    if failed:
        result.update(status="FAILED", failed_step=failed["variant"],
                      process_type=failed["process_type"], error_message=failed["error_message"])
    elif expected and running and export_at > expected:
        result.update(status="LATE", minutes_late=int((export_at - expected).total_seconds() // 60),
                      late_note=f"still running at {export_at:%H:%M}, so at least this many minutes late")
    elif expected and finished_at and finished_at > expected:
        result.update(status="LATE", minutes_late=int((finished_at - expected).total_seconds() // 60))
    elif warning:
        result.update(status="WARNING", failed_step=warning["variant"],
                      process_type=warning["process_type"], warning_message=warning["error_message"])
    else:
        result.update(status="RUNNING" if running else "SUCCESS")
    return result


def _analyze(run_date: str | None = None) -> dict:
    log, schedule, impact, runbook = _load_run_log(), _load_schedule(), _load_impact_map(), _load_runbook()
    export_at = _export_time(runbook, log)
    runs = _runs_by_date(log)
    dates = sorted(runs)
    run_date = run_date or dates[-1]
    if run_date not in runs:
        return {"error": f"No runs found for {run_date}. Available dates: {', '.join(dates)}"}

    chains = []
    for chain_id, steps in runs[run_date].items():
        c = _classify(chain_id, steps, schedule, export_at)
        reports = _reports_for(chain_id, impact)
        c["affected_reports"] = [r["report_or_dashboard"] for r in reports]
        c["business_owners"] = sorted({r["business_owner"] for r in reports})
        c["user_groups"] = sorted({r["user_group"] for r in reports})

        if c["status"] == "FAILED":
            entry = _match_runbook(c["error_message"], runbook)
            if entry:
                owner = entry["owner"]
                if "data owner for the area" in owner.lower():
                    person = _area_owner(c["area"] or "", runbook)
                    if person:
                        owner = owner.replace("Data owner for the area", f"{person} (data owner, {c['area']})")
                c.update(in_runbook=True, runbook_error=entry["error"], likely_cause=entry["likely_cause"],
                         standard_fix=entry["standard_fix"], owner=owner)
            else:
                c.update(in_runbook=False, likely_cause="not in the runbook",
                         standard_fix="not in the runbook", owner="not in the runbook")

            earlier = [d for d in dates if d < run_date]
            same_error_dates = []
            for d in earlier:
                prev = runs[d].get(chain_id, [])
                if any(s["status"] == "FAILED" and s["error_message"] == c["error_message"] for s in prev):
                    same_error_dates.append(d)
            c["earlier_runs_with_same_error"] = len(same_error_dates)
            c["earlier_failure_dates"] = same_error_dates
            previous_date = earlier[-1] if earlier else None
            if previous_date and previous_date in same_error_dates and runbook["escalation_contact"]:
                c["escalate_to"] = runbook["escalation_contact"]
                c["standard_fix"] += f". Escalate to {runbook['escalation_contact']}"
        elif c["status"] in ("LATE", "WARNING"):
            c.update(standard_fix="no runbook action", owner="no runbook action")
        chains.append(c)

    attention = sorted(
        [c for c in chains if c["status"] in STATUS_ORDER],
        key=lambda c: (STATUS_ORDER[c["status"]], -len(c["affected_reports"]), c["chain_id"]),
    )
    stale = []
    for c in chains:
        if c["status"] == "FAILED" or c["still_running"]:
            for r in c["affected_reports"]:
                if r not in stale:
                    stale.append(r)

    return {
        "run_date": run_date,
        "log_exported_at": export_at.strftime(TIME_FMT),
        "chains_needing_attention": attention,
        "other_chains": [
            {k: c[k] for k in ("chain_id", "chain_description", "status", "expected_finish", "finished_at")}
            for c in chains if c["status"] not in STATUS_ORDER
        ],
        "stale_reports": stale,
        "summary_line": f"{len(attention)} chains need attention. {len(stale)} reports are showing stale data.",
    }


# --------------------------------------------------------------------------
# Tools the agents can call
# --------------------------------------------------------------------------

def get_overnight_status(run_date: str = "") -> dict:
    """Classify every process chain run for one night and match failures to the runbook.

    Args:
        run_date: Night to check, as YYYY-MM-DD. Leave empty for the latest night ("last night").

    Returns:
        chains_needing_attention (already sorted FAILED, LATE, WARNING, then by most
        affected reports), other_chains, stale_reports and the exact summary_line.
    """
    return _analyze(run_date or None)


def get_chain_details(chain: str) -> dict:
    """Get the latest run of one process chain and its history in the log.

    Args:
        chain: Chain ID (for example ZPC_SD_DAILY) or words from its description
            (for example "daily sales" or "headcount").

    Returns:
        The chain's latest run with status, cause, fix, owner and affected reports,
        plus every earlier run in the log.
    """
    result = _analyze()
    if "error" in result:
        return result
    all_chains = result["chains_needing_attention"] + result["other_chains"]
    words = chain.lower().replace("load", "").replace("chain", "").split()
    match = next((c for c in all_chains if c["chain_id"].lower() == chain.lower()), None)
    if not match:
        match = next((c for c in all_chains if all(w in c["chain_description"].lower() for w in words)), None)
    if not match:
        return {"error": f"No chain matches '{chain}'.",
                "known_chains": [f"{c['chain_id']} ({c['chain_description']})" for c in all_chains]}

    full = next((c for c in result["chains_needing_attention"] if c["chain_id"] == match["chain_id"]), match)
    history = []
    for d, chains in sorted(_runs_by_date(_load_run_log()).items()):
        for s in chains.get(match["chain_id"], []):
            history.append({k: s[k] for k in ("process_type", "start_time", "end_time", "status", "error_message")})
    return {"latest_run": full, "history": history, "log_exported_at": result["log_exported_at"]}


def get_stale_reports(user_group: str = "") -> dict:
    """List reports showing stale data: those fed by a failed chain or a chain still running.

    Args:
        user_group: Optional, for example "Sales users". Leave empty for all groups.
    """
    result = _analyze()
    if "error" in result:
        return result
    rows = []
    for c in result["chains_needing_attention"]:
        if c["status"] == "FAILED" or c["still_running"]:
            for r in _reports_for(c["chain_id"], _load_impact_map()):
                if user_group and r["user_group"].lower() != user_group.lower():
                    continue
                rows.append({"report": r["report_or_dashboard"], "chain_id": c["chain_id"],
                             "chain_status": c["status"], "business_owner": r["business_owner"],
                             "user_group": r["user_group"]})
    unique = list(dict.fromkeys(r["report"] for r in rows))
    current_again = [
        {"chain_id": c["chain_id"], "finished_at": c["finished_at"], "reports": c["affected_reports"]}
        for c in result["chains_needing_attention"]
        if c["status"] == "LATE" and not c["still_running"]
    ]
    return {"stale_report_count": len(unique), "stale_reports": unique, "details": rows,
            "late_chains_now_finished": current_again, "log_exported_at": result["log_exported_at"]}


def get_business_update_facts(user_group: str) -> dict:
    """Facts for a business update to one user group about last night's data.

    Args:
        user_group: The group named by the user, for example "Sales users" or "sales".

    Returns:
        not_updated reports (failed or still-running chains) and may_be_incomplete
        reports (warnings). Late chains that have since finished are left out.
    """
    impact = _load_impact_map()
    groups = sorted({r["user_group"] for r in impact})
    wanted = user_group.lower().replace("users", "").strip()
    group = next((g for g in groups if g.lower().replace("users", "").strip() == wanted), None)
    if not group:
        return {"error": f"Unknown user group '{user_group}'.", "known_user_groups": groups}

    result = _analyze()
    not_updated, incomplete = [], []
    for c in result["chains_needing_attention"]:
        reports = [r["report_or_dashboard"] for r in _reports_for(c["chain_id"], impact) if r["user_group"] == group]
        if not reports:
            continue
        if c["status"] == "FAILED" or c["still_running"]:
            not_updated += [r for r in reports if r not in not_updated]
        elif c["status"] == "WARNING":
            incomplete += [r for r in reports if r not in incomplete and r not in not_updated]
    return {"user_group": group, "run_date": result["run_date"],
            "not_updated": not_updated, "may_be_incomplete": incomplete,
            "nothing_affected": not (not_updated or incomplete)}
