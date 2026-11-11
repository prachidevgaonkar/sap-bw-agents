# BW Load Triage Assistant: ADK version

The same agent as the no-code [Workflow Builder version](../README.md), built in Python with Google's [Agent Development Kit (ADK)](https://adk.dev). Use this version when you need:

- **A link you can share outside your organization.** Deploy it to Cloud Run with a web UI.
- **Exact answers.** Python tools classify the runs, match the runbook and count reports. The model only explains the results, so it can't miscount or invent a fix.
- **A path to real SAP BW data.** Swap the sample files for a read-only connection in one file.

**Status:** the tools pass all 9 checks against the [answer key](../sample-data/answer_key.csv), and the routing works with a scripted test model. Not yet tested with a live Gemini model: run the [test script](../sample-data/TESTING.md) after setup.

## How it works

```
bw_load_triage_assistant (routes only)
├── chain_failure_analyst      tools: get_overnight_status, get_chain_details, get_stale_reports
└── business_update_drafter    tools: get_business_update_facts
```

Like Workflow Builder, the main agent transfers each request and the specialist answers the user directly. In ADK a specialist can also hand off to its peer, so "now draft an update for sales" works after an overview question.

| File | What it does |
| --- | --- |
| `bw_triage/agent.py` | The three agents and their instructions |
| `bw_triage/tools.py` | Read-only tools: all the logic, with no model involved |
| `bw_triage/data/` | The fictional sample data (same as `../sample-data/`) |
| `tests/test_tools.py` | Checks the tools against the answer key |

## Run it on your computer

You need Python 3.10 or later and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) (or a Google Cloud project, see `.env.example`).

```bash
git clone https://github.com/prachidevgaonkar/sap-bw-agents.git
cd sap-bw-agents/bw-load-triage/adk
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r bw_triage/requirements.txt
cp bw_triage/.env.example bw_triage/.env           # then paste your API key into bw_triage/.env
adk web .
```

Open http://localhost:8000, pick **bw_triage**, and ask the questions from the test script. The left panel shows each transfer and tool call, which is the ADK version of "Show thinking".

To check the tools without a model: `pip install pytest && pytest tests`.

## Share a public demo link (Cloud Run)

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
adk deploy cloud_run --project YOUR_PROJECT_ID --region us-central1 \
  --service_name bw-triage-demo --with_ui ./bw_triage
```

When asked whether to allow unauthenticated invocations, answer **y** for a public demo. You get a URL anyone can open.

Before you post the link:
- Anyone with the link uses your Gemini quota. Set a [budget alert](https://cloud.google.com/billing/docs/how-to/budgets) and consider a low maximum number of Cloud Run instances.
- The ADK web UI is a developer tool: visitors see the tool calls and results. That's fine (and interesting) for this fictional data.
- Never deploy a public link that reads real BW data.

## Use it inside Gemini Enterprise

Deploy to Agent Engine (`adk deploy agent_engine`), then a Gemini Enterprise admin registers it as a custom ADK agent in the app. Users then find it in the agent gallery next to the Workflow Builder agents. Check that your Gemini Enterprise edition allows registering custom agents.

## Connect real SAP BW data

Everything the agents know comes from four functions at the top of `tools.py`: `_load_run_log`, `_load_schedule`, `_load_impact_map` and `_load_runbook`. Replace them with a read-only source and keep the same columns, for example:

- a daily export of the chain run log to Cloud Storage or Google Drive, or
- an OData service over the process chain log tables, called with a technical user that can only read.

The agents and their instructions don't change. Keep it read-only: no tool should be able to restart a chain.
