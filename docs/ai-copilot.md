# SupplyChain360 AI Copilot

SupplyChain360 includes a read-only, evidence-first agentic analytics layer on top of the existing SQL and Power BI solution.

## Architecture

User question -> FastAPI -> deterministic domain router -> governed specialist tool -> analytics SQL view -> structured evidence -> concise explanation

Specialist domains are inventory, procurement, fulfillment, and sales/demand. A proactive exception endpoint runs the first three specialist tools together for operational triage.

## Safety and governance

- Database access is SELECT/CTE only.
- The agent cannot execute arbitrary write SQL.
- Domain tools use parameterized queries over validated analytics views.
- KPI values come from SQL evidence, not from a language model.
- Responses return domain, tool metadata and evidence rows for traceability.
- The core works without an LLM; a model can later improve explanation quality without becoming the metric source.

## API

Install and run:

    python -m pip install -r requirements-agent.txt
    uvicorn api.main:app --reload

Endpoints:

- GET /health - service health.
- POST /ask - route a business question and execute its governed SQL tool.
- GET /exceptions - collect inventory, procurement and fulfillment exceptions.

Use execute=false in POST /ask to demonstrate routing without a live SQL Server connection.

Example:

    {"question":"Which SKUs are understocked and need reorder?","limit":10,"execute":true}

## Configuration

Use the variables documented in .env.example. Windows integrated authentication is the default local configuration. No credentials are committed.

## Evaluation

evals/golden_questions.json contains representative questions with expected specialist domains. CI runs router, service and golden-question regression tests alongside the existing Power BI validators.

## Why this is agentic

The application performs bounded decision routing, selects a specialist analytical capability, executes a governed data tool and returns traceable evidence. Metric computation stays separate from natural-language explanation.

## Production extensions

A production deployment can add an approved hosted LLM for richer synthesis, authentication, persistent audit logs, Power BI Service integration and scheduled notification delivery. Those require external deployment credentials/services and are intentionally not hard-coded into the repository.
