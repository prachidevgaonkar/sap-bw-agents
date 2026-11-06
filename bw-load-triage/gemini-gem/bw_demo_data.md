# BW Load Triage demo data

All systems, chains, people and data in this file are fictional. It has four parts: Chain Schedule, Report Impact Map, Chain Run Log and Runbook.

## Chain Schedule

| chain_id | chain_description | area | expected_finish_time |
| --- | --- | --- | --- |
| ZPC_MD_MATERIAL | Material master data | Master data | 01:30 |
| ZPC_SD_DAILY | Daily sales load | Sales | 05:00 |
| ZPC_SD_ORDERS | Sales orders | Sales | 05:30 |
| ZPC_SD_BILLING | Billing documents | Sales | 05:30 |
| ZPC_FI_GL | GL actuals load | Finance | 06:00 |
| ZPC_FI_AR | Open receivables | Finance | 06:00 |
| ZPC_CO_MARGIN | Margin analysis | Controlling | 06:15 |
| ZPC_MM_STOCK | Inventory snapshot | Inventory | 05:45 |
| ZPC_PUR_PO | Purchase orders | Purchasing | 05:45 |
| ZPC_HR_HEADCOUNT | Headcount | HR | 06:00 |
| ZPC_SCM_FCST | Demand forecast load | Planning | 06:30 |

## Report Impact Map

| chain_id | report_or_dashboard | business_owner | user_group |
| --- | --- | --- | --- |
| ZPC_SD_DAILY | Daily sales dashboard | Maria Lopez (Sales Ops) | Sales users |
| ZPC_SD_DAILY | Sales by region | Maria Lopez (Sales Ops) | Sales users |
| ZPC_SD_DAILY | Sales vs. target | Maria Lopez (Sales Ops) | Sales users |
| ZPC_SD_DAILY | Weekly sales email | Maria Lopez (Sales Ops) | Sales users |
| ZPC_SD_DAILY | Executive KPI cockpit | Maria Lopez (Sales Ops) | Sales users |
| ZPC_CO_MARGIN | Margin analysis | Tom Becker (Controlling) | Controlling users |
| ZPC_CO_MARGIN | Product profitability | Tom Becker (Controlling) | Controlling users |
| ZPC_CO_MARGIN | Customer profitability | Tom Becker (Controlling) | Controlling users |
| ZPC_CO_MARGIN | Executive KPI cockpit | Tom Becker (Controlling) | Controlling users |
| ZPC_MM_STOCK | Inventory snapshot | Aisha Khan (Supply Chain) | Inventory users |
| ZPC_MM_STOCK | Stock aging | Aisha Khan (Supply Chain) | Inventory users |
| ZPC_MM_STOCK | Warehouse utilization | Aisha Khan (Supply Chain) | Inventory users |
| ZPC_PUR_PO | Open purchase orders | Aisha Khan (Supply Chain) | Purchasing users |
| ZPC_PUR_PO | Supplier performance | Aisha Khan (Supply Chain) | Purchasing users |
| ZPC_HR_HEADCOUNT | Monthly headcount | Grace Liu (HR) | HR users |
| ZPC_FI_GL | P&L statement | Tom Becker (Controlling) | Finance users |
| ZPC_FI_GL | GL trial balance | Tom Becker (Controlling) | Finance users |
| ZPC_FI_GL | Executive KPI cockpit | Tom Becker (Controlling) | Finance users |
| ZPC_SCM_FCST | Demand forecast accuracy | Aisha Khan (Supply Chain) | Planning users |
| ZPC_SD_BILLING | Billing overview | Maria Lopez (Sales Ops) | Sales users |
| ZPC_SD_BILLING | Revenue by product | Maria Lopez (Sales Ops) | Sales users |
| ZPC_SD_ORDERS | Order backlog | Maria Lopez (Sales Ops) | Sales users |
| ZPC_FI_AR | AR aging | Tom Becker (Controlling) | Finance users |

## Chain Run Log

A "-" means empty: no end time yet, or no error message.

| chain_id | chain_description | process_type | variant | start_time | end_time | status | error_message |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZPC_MD_MATERIAL | Material master data | DTP_LOAD | ZPC_MD_MATERIAL_LOAD | 2026-11-01 00:00 | 2026-11-01 00:20 | SUCCESS | - |
| ZPC_MD_MATERIAL | Material master data | ADSO_ACTIVATE | ZPC_MD_MATERIAL_ACT | 2026-11-01 00:20 | 2026-11-01 00:35 | SUCCESS | - |
| ZPC_SD_DAILY | Daily sales load | DTP_LOAD | ZPC_SD_DAILY_LOAD | 2026-11-01 04:00 | 2026-11-01 04:20 | SUCCESS | - |
| ZPC_SD_DAILY | Daily sales load | ADSO_ACTIVATE | ZPC_SD_DAILY_ACT | 2026-11-01 04:20 | 2026-11-01 04:35 | SUCCESS | - |
| ZPC_SD_ORDERS | Sales orders | DTP_LOAD | ZPC_SD_ORDERS_LOAD | 2026-11-01 04:00 | 2026-11-01 04:20 | SUCCESS | - |
| ZPC_SD_ORDERS | Sales orders | ADSO_ACTIVATE | ZPC_SD_ORDERS_ACT | 2026-11-01 04:20 | 2026-11-01 04:35 | SUCCESS | - |
| ZPC_SD_BILLING | Billing documents | DTP_LOAD | ZPC_SD_BILLING_LOAD | 2026-11-01 04:00 | 2026-11-01 04:20 | SUCCESS | - |
| ZPC_SD_BILLING | Billing documents | ADSO_ACTIVATE | ZPC_SD_BILLING_ACT | 2026-11-01 04:20 | 2026-11-01 04:35 | SUCCESS | - |
| ZPC_FI_GL | GL actuals load | DTP_LOAD | ZPC_FI_GL_LOAD | 2026-11-01 05:00 | 2026-11-01 05:20 | SUCCESS | - |
| ZPC_FI_GL | GL actuals load | ADSO_ACTIVATE | ZPC_FI_GL_ACT | 2026-11-01 05:20 | 2026-11-01 05:35 | SUCCESS | - |
| ZPC_FI_AR | Open receivables | DTP_LOAD | ZPC_FI_AR_LOAD | 2026-11-01 05:00 | 2026-11-01 05:20 | SUCCESS | - |
| ZPC_FI_AR | Open receivables | ADSO_ACTIVATE | ZPC_FI_AR_ACT | 2026-11-01 05:20 | 2026-11-01 05:35 | SUCCESS | - |
| ZPC_CO_MARGIN | Margin analysis | DTP_LOAD | ZPC_CO_MARGIN_LOAD | 2026-11-01 05:00 | 2026-11-01 05:20 | SUCCESS | - |
| ZPC_CO_MARGIN | Margin analysis | ADSO_ACTIVATE | ZPC_CO_MARGIN_ACT | 2026-11-01 05:20 | 2026-11-01 05:35 | SUCCESS | - |
| ZPC_MM_STOCK | Inventory snapshot | DTP_LOAD | ZPC_MM_STOCK_LOAD | 2026-11-01 04:00 | 2026-11-01 04:20 | SUCCESS | - |
| ZPC_MM_STOCK | Inventory snapshot | ADSO_ACTIVATE | ZPC_MM_STOCK_ACT | 2026-11-01 04:20 | 2026-11-01 04:35 | SUCCESS | - |
| ZPC_PUR_PO | Purchase orders | DTP_LOAD | ZPC_PUR_PO_LOAD | 2026-11-01 04:00 | 2026-11-01 04:20 | SUCCESS | - |
| ZPC_PUR_PO | Purchase orders | ADSO_ACTIVATE | ZPC_PUR_PO_ACT | 2026-11-01 04:20 | 2026-11-01 04:35 | SUCCESS | - |
| ZPC_HR_HEADCOUNT | Headcount | DTP_LOAD | ZPC_HR_HEADCOUNT_LOAD | 2026-11-01 05:00 | 2026-11-01 05:20 | SUCCESS | - |
| ZPC_HR_HEADCOUNT | Headcount | ADSO_ACTIVATE | ZPC_HR_HEADCOUNT_ACT | 2026-11-01 05:20 | 2026-11-01 05:35 | SUCCESS | - |
| ZPC_SCM_FCST | Demand forecast load | DTP_LOAD | ZPC_SCM_FCST_LOAD | 2026-11-01 05:00 | 2026-11-01 05:20 | SUCCESS | - |
| ZPC_SCM_FCST | Demand forecast load | ADSO_ACTIVATE | ZPC_SCM_FCST_ACT | 2026-11-01 05:20 | 2026-11-01 05:35 | SUCCESS | - |
| ZPC_MD_MATERIAL | Material master data | DTP_LOAD | ZPC_MD_MATERIAL_LOAD | 2026-11-02 00:00 | 2026-11-02 00:20 | SUCCESS | - |
| ZPC_MD_MATERIAL | Material master data | ADSO_ACTIVATE | ZPC_MD_MATERIAL_ACT | 2026-11-02 00:20 | 2026-11-02 00:35 | SUCCESS | - |
| ZPC_SD_DAILY | Daily sales load | DTP_LOAD | ZPC_SD_DAILY_LOAD | 2026-11-02 03:00 | 2026-11-02 03:12 | FAILED | Object ZSD_D01 is locked by request REQU_4FQ2 (attribute change run) |
| ZPC_SD_DAILY | Daily sales load | ADSO_ACTIVATE | ZPC_SD_DAILY_ACT | - | - | NOT RUN | - |
| ZPC_SD_ORDERS | Sales orders | DTP_LOAD | ZPC_SD_ORDERS_LOAD | 2026-11-02 04:00 | 2026-11-02 04:20 | SUCCESS | - |
| ZPC_SD_ORDERS | Sales orders | ADSO_ACTIVATE | ZPC_SD_ORDERS_ACT | 2026-11-02 04:20 | 2026-11-02 04:35 | SUCCESS | - |
| ZPC_SD_BILLING | Billing documents | DTP_LOAD | ZPC_SD_BILLING_LOAD | 2026-11-02 04:00 | 2026-11-02 04:20 | SUCCESS | - |
| ZPC_SD_BILLING | Billing documents | ADSO_ACTIVATE | ZPC_SD_BILLING_ACT | 2026-11-02 04:20 | 2026-11-02 04:35 | SUCCESS | - |
| ZPC_FI_GL | GL actuals load | DTP_LOAD | ZPC_FI_GL_LOAD | 2026-11-02 05:00 | 2026-11-02 05:20 | SUCCESS | - |
| ZPC_FI_GL | GL actuals load | ADSO_ACTIVATE | ZPC_FI_GL_ACT | 2026-11-02 05:20 | 2026-11-02 05:35 | SUCCESS | - |
| ZPC_FI_AR | Open receivables | DTP_LOAD | ZPC_FI_AR_LOAD | 2026-11-02 05:00 | 2026-11-02 05:20 | SUCCESS | - |
| ZPC_FI_AR | Open receivables | ADSO_ACTIVATE | ZPC_FI_AR_ACT | 2026-11-02 05:20 | 2026-11-02 05:35 | SUCCESS | - |
| ZPC_CO_MARGIN | Margin analysis | DTP_LOAD | ZPC_CO_MARGIN_LOAD | 2026-11-02 05:00 | 2026-11-02 05:20 | SUCCESS | - |
| ZPC_CO_MARGIN | Margin analysis | ADSO_ACTIVATE | ZPC_CO_MARGIN_ACT | 2026-11-02 05:20 | 2026-11-02 05:35 | SUCCESS | - |
| ZPC_MM_STOCK | Inventory snapshot | DTP_LOAD | ZPC_MM_STOCK_LOAD | 2026-11-02 04:00 | 2026-11-02 04:20 | SUCCESS | - |
| ZPC_MM_STOCK | Inventory snapshot | ADSO_ACTIVATE | ZPC_MM_STOCK_ACT | 2026-11-02 04:20 | 2026-11-02 04:35 | SUCCESS | - |
| ZPC_PUR_PO | Purchase orders | DTP_LOAD | ZPC_PUR_PO_LOAD | 2026-11-02 04:00 | 2026-11-02 04:20 | SUCCESS | - |
| ZPC_PUR_PO | Purchase orders | ADSO_ACTIVATE | ZPC_PUR_PO_ACT | 2026-11-02 04:20 | 2026-11-02 04:35 | SUCCESS | - |
| ZPC_HR_HEADCOUNT | Headcount | DTP_LOAD | ZPC_HR_HEADCOUNT_LOAD | 2026-11-02 05:00 | 2026-11-02 05:20 | SUCCESS | - |
| ZPC_HR_HEADCOUNT | Headcount | ADSO_ACTIVATE | ZPC_HR_HEADCOUNT_ACT | 2026-11-02 05:20 | 2026-11-02 05:35 | SUCCESS | - |
| ZPC_SCM_FCST | Demand forecast load | DTP_LOAD | ZPC_SCM_FCST_LOAD | 2026-11-02 05:00 | 2026-11-02 05:20 | SUCCESS | - |
| ZPC_SCM_FCST | Demand forecast load | ADSO_ACTIVATE | ZPC_SCM_FCST_ACT | 2026-11-02 05:20 | 2026-11-02 05:35 | SUCCESS | - |
| ZPC_MD_MATERIAL | Material master data | DTP_LOAD | ZPC_MD_MATERIAL_LOAD | 2026-11-03 00:30 | 2026-11-03 00:55 | SUCCESS | - |
| ZPC_MD_MATERIAL | Material master data | ADSO_ACTIVATE | ZPC_MD_MATERIAL_ACT | 2026-11-03 00:55 | 2026-11-03 01:10 | SUCCESS | - |
| ZPC_SD_DAILY | Daily sales load | DTP_LOAD | ZPC_SD_DAILY_LOAD | 2026-11-03 03:00 | 2026-11-03 03:11 | FAILED | Object ZSD_D01 is locked by request REQU_4FQ2 (attribute change run) |
| ZPC_SD_DAILY | Daily sales load | ADSO_ACTIVATE | ZPC_SD_DAILY_ACT | - | - | NOT RUN | - |
| ZPC_SD_ORDERS | Sales orders | DTP_LOAD | ZPC_SD_ORDERS_LOAD | 2026-11-03 04:00 | 2026-11-03 04:25 | SUCCESS | - |
| ZPC_SD_ORDERS | Sales orders | ADSO_ACTIVATE | ZPC_SD_ORDERS_ACT | 2026-11-03 04:25 | 2026-11-03 04:40 | SUCCESS | - |
| ZPC_SD_BILLING | Billing documents | DTP_LOAD | ZPC_SD_BILLING_LOAD | 2026-11-03 04:15 | 2026-11-03 04:45 | WARNING | Request contains 3 records with errors; records written to the error stack |
| ZPC_SD_BILLING | Billing documents | ADSO_ACTIVATE | ZPC_SD_BILLING_ACT | 2026-11-03 04:45 | 2026-11-03 05:05 | SUCCESS | - |
| ZPC_FI_GL | GL actuals load | DTP_LOAD | ZPC_FI_GL_LOAD | 2026-11-03 04:30 | 2026-11-03 06:10 | SUCCESS | - |
| ZPC_FI_GL | GL actuals load | ADSO_ACTIVATE | ZPC_FI_GL_ACT | 2026-11-03 06:10 | 2026-11-03 06:42 | SUCCESS | - |
| ZPC_FI_AR | Open receivables | DTP_LOAD | ZPC_FI_AR_LOAD | 2026-11-03 05:00 | 2026-11-03 05:20 | SUCCESS | - |
| ZPC_FI_AR | Open receivables | ADSO_ACTIVATE | ZPC_FI_AR_ACT | 2026-11-03 05:20 | 2026-11-03 05:35 | SUCCESS | - |
| ZPC_CO_MARGIN | Margin analysis | DTP_LOAD | ZPC_CO_MARGIN_LOAD | 2026-11-03 05:10 | 2026-11-03 05:40 | SUCCESS | - |
| ZPC_CO_MARGIN | Margin analysis | ADSO_ACTIVATE | ZPC_CO_MARGIN_ACT | 2026-11-03 05:40 | 2026-11-03 05:52 | FAILED | Activation of data in aDSO ZCO_MARG failed: duplicate data record with same semantic key |
| ZPC_MM_STOCK | Inventory snapshot | DTP_LOAD | ZPC_MM_STOCK_LOAD | 2026-11-03 04:20 | 2026-11-03 04:31 | FAILED | No SID found for value 'MAT-90017' of characteristic 0MATERIAL |
| ZPC_MM_STOCK | Inventory snapshot | ADSO_ACTIVATE | ZPC_MM_STOCK_ACT | - | - | NOT RUN | - |
| ZPC_PUR_PO | Purchase orders | DTP_LOAD | ZPC_PUR_PO_LOAD | 2026-11-03 04:40 | 2026-11-03 04:41 | FAILED | RFC connection to source system ECCPRD100 failed: partner not reached |
| ZPC_PUR_PO | Purchase orders | ADSO_ACTIVATE | ZPC_PUR_PO_ACT | - | - | NOT RUN | - |
| ZPC_HR_HEADCOUNT | Headcount | DTP_LOAD | ZPC_HR_HEADCOUNT_LOAD | 2026-11-03 05:05 | 2026-11-03 05:09 | FAILED | Value 'sales&marketing' (characteristic ZORGUNIT) contains invalid characters |
| ZPC_HR_HEADCOUNT | Headcount | ADSO_ACTIVATE | ZPC_HR_HEADCOUNT_ACT | - | - | NOT RUN | - |
| ZPC_SCM_FCST | Demand forecast load | DTP_LOAD | ZPC_SCM_FCST_LOAD | 2026-11-03 05:30 | - | RUNNING | - |
| ZPC_SCM_FCST | Demand forecast load | ADSO_ACTIVATE | ZPC_SCM_FCST_ACT | - | - | NOT RUN | - |

## Runbook

All systems, chains and people in this sample are fictional.

### Test dataset date
For this sample dataset, "last night" means the loads that ran overnight into **Tuesday, November 3, 2026**. The run log was exported at **07:00 on November 3, 2026**. Chains still running at that time have no end time.

### Known errors

| Error | How to recognize it | Likely cause | Standard fix | Owner |
| --- | --- | --- | --- | --- |
| Lock conflict | Message contains "is locked by" | Another load or process (for example, an attribute change run) was using the same object at the same time | Wait until the other process has finished, then repeat the failed step | BW support |
| Source system connection | Message contains "RFC connection" and "failed" | Source system unavailable or connection problem | Ask the Basis team to check the connection, then repeat the failed step | Basis team |
| Missing master data | Message contains "No SID found" | Transaction data arrived before the master data for that value | Run the master data chain for that characteristic, then repeat the failed step | BW support |
| Invalid characters | Message contains "invalid characters" | A source value contains characters BW does not accept | Ask the data owner for the area to correct the value in the source system, then repeat the load. Do not change the permitted characters setting. | Data owner for the area, with BW support |

### Escalation
If the same chain fails with the same error in **two consecutive runs**, escalate to the BW lead, **Ravi Menon**, in addition to the standard fix.

### Data owners by area
- Sales: Maria Lopez
- Finance and Controlling: Tom Becker
- Inventory, Purchasing and Planning: Aisha Khan
- HR: Grace Liu
