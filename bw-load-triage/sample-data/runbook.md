# BW Support Runbook (sample)

Upload this as a Knowledge file. Replace it with your team's real runbook. All systems, chains and people in this sample are fictional.

## Test dataset date
For this sample dataset, "last night" means the loads that ran overnight into **Tuesday, November 3, 2026**. The run log was exported at **07:00 on November 3, 2026**. Chains still running at that time have no end time.

## Known errors

| Error | How to recognize it | Likely cause | Standard fix | Owner |
| --- | --- | --- | --- | --- |
| Lock conflict | Message contains "is locked by" | Another load was writing to the same object at the same time | Wait until the other load has finished, then repeat the failed step | BW support |
| Source system connection | Message contains "RFC connection" and "failed" | Source system unavailable or connection problem | Ask the Basis team to check the connection, then repeat the failed step | Basis team |
| Missing master data | Message contains "No SID found" | Transaction data arrived before the master data for that value | Run the master data chain for that characteristic, then repeat the failed step | BW support |
| Invalid characters | Message contains "invalid characters" | A source value contains characters BW does not accept | Ask the data owner for the area to correct the value in the source system, then repeat the load. Do not change the permitted characters setting. | Data owner for the area, with BW support |

## Escalation
If the same chain fails with the same error in **two consecutive runs**, escalate to the BW lead, **Ravi Menon**, in addition to the standard fix.

## Data owners by area
- Sales: Maria Lopez
- Finance and Controlling: Tom Becker
- Inventory, Purchasing and Planning: Aisha Khan
- HR: Grace Liu
