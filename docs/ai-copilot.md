# SupplyChain360 AI Copilot

## Goal

Add a read-only, evidence-first AI analytics layer without replacing the existing SQL, semantic model or Power BI report.

## Design principles

1. **Governed tools before free-form SQL.** Agents call allow-listed analytical capabilities backed by validated project views/KPIs.
2. **Numbers come from analytics code.** The language model explains evidence; it is not the source of KPI values.
3. **Read-only by default.** The copilot does not modify operational data.
4. **Traceable answers.** Responses will expose the domain/tool and evidence used.
5. **Evaluate before adding autonomy.** Golden business questions and regression tests are added as capabilities grow.

## Target flow

User question -> router -> specialist analytics tool -> SQL evidence -> explanation -> API/chat UI

Specialist domains: inventory, procurement, fulfillment, and sales/demand.

## Delivery stages

- **Stage 1 (this branch):** package structure, deterministic router, governed tool catalog, FastAPI shell and tests.
- **Stage 2:** SQL Server read-only connector, parameterized domain queries, evidence schema and integration tests.
- **Stage 3:** LLM synthesis with citations to returned evidence, specialist graph/orchestration and golden-question evaluation.
- **Stage 4:** scheduled exception detection and concise operational alerts.

## Local foundation run

    python -m pip install -r requirements-agent.txt
    pytest tests/test_agent_router.py -q
    uvicorn api.main:app --reload

Then open the local API documentation at /docs and try POST /ask.
