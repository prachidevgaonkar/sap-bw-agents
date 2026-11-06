# Test script for the BW Load Triage Assistant

All systems, chains, people and data here are fictional. The runbook sets "last night" as the loads that ran into **November 3, 2026**, with the run log exported at **07:00**.

The files:
- `chain_run_log.csv`, `chain_schedule.csv`, `report_impact_map.csv`: the agent's data sources
- `runbook.md`: the agent's knowledge file
- `answer_key.csv` and this file: **for you only**, never give them to the agent

Ask these questions in the **Preview** tab and compare the answers.

| # | Ask | A correct answer |
| --- | --- | --- |
| 1 | Which chains need attention from last night? | 8 chains. Failed, by number of affected reports: Daily sales load (5), Margin analysis (4), Inventory snapshot (3), Purchase orders (2), Headcount (1). Late: GL actuals load (42 minutes), Demand forecast load (still running, at least 30 minutes late). Warning: Billing documents. |
| 2 | Why did the daily sales load fail? | Lock conflict: the object was locked by another request (an attribute change run). Fix: wait until the other process has finished, then repeat the failed step. It failed with the same error on the previous run, so escalate to Ravi Menon. |
| 3 | What happened with the margin analysis chain? | Activation failed with a duplicate record error. This error is **not in the runbook**, and the agent quotes the message instead of guessing a cause or fix. |
| 4 | Why did the inventory snapshot fail? | Missing master data: no SID for material MAT-90017. Fix: run the material master data chain, then repeat. Affected: Inventory snapshot, Stock aging, Warehouse utilization. |
| 5 | Who needs to fix the purchase orders load? | The Basis team: the RFC connection to ECCPRD100 failed. Then repeat the failed step. |
| 6 | What's the fix for the headcount load? | Invalid characters in "sales&marketing". The HR data owner (Grace Liu) corrects the value in the source, then the load is repeated. Do **not** change the permitted characters setting. |
| 7 | Which reports are showing stale data right now? | 15 reports from the failed chains and the still-running forecast load. The Executive KPI cockpit is listed once, even though three chains feed it. The GL reports are current again, because that chain finished, late. (Also acceptable: 17, if the agent counts the late GL chain's reports and says that chain has since finished.) |
| 8 | Draft an update for the sales users. | One message covering the Daily sales dashboard, Sales by region, Sales vs. target, Weekly sales email and Executive KPI cockpit. No lock or technical details, and no promised time unless you give one. |
| 9 | Did the material master data chain run? | Yes, it succeeded at 01:10. It still has to be run again for MAT-90017, per the fix in question 4. |

## Pass bar
- Questions 1 to 6 and 9 answered correctly, with the right status, cause and fix.
- Question 3 says "not in the runbook". Any guessed cause is a fail.
- No invented times, chains or reports.

Note any wrong answer, what you changed in the instructions, and whether the retest passed. That log becomes your results post.
