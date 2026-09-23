# SupplyChain360 — Demo & Interview Guide

This guide explains the project in a way that is accurate to the implementation and easy to demonstrate in an interview.

## 60-second project story

SupplyChain360 started as an end-to-end supply-chain BI project on Microsoft's WideWorldImportersDW sample warehouse. I built a governed SQL analytics layer, a star-schema Power BI model, 113 DAX measures, dynamic RLS, automated validation, and a 14-page operational report.

I then added an evidence-first analytics copilot. Instead of letting a language model invent SQL or KPIs, a FastAPI service routes a business question to an allow-listed specialist tool for inventory, procurement, fulfillment, or sales. That tool queries the validated SQL analytics views in read-only mode and returns the evidence behind the answer. An exception endpoint also combines inventory, procurement, and fulfillment risks for operational triage.

## 3-minute interview walkthrough

### 1. Business problem

Supply-chain teams usually need to connect inventory, suppliers, purchase orders, fulfillment, sales, profitability, and stock movement. The goal was to create one analytical layer where those questions can be answered consistently rather than through disconnected reports.

### 2. Data and engineering

The source is WideWorldImportersDW on SQL Server. Reusable T-SQL analytics views prepare the five analytical domains. Power Query loads selected columns into a dimensional model, and the semantic layer contains explicit DAX measures for operational KPIs.

The Power BI project is stored as PBIP/PBIR/TMDL text rather than committing PBIX binaries, which makes model and report changes reviewable in Git.

### 3. BI layer

The report has 14 pages, including executive overview, inventory intelligence, procurement and supplier performance, fulfillment/backorders, sales and demand, profitability, stock movement, Product 360, Supplier 360, and data-quality QA.

Dynamic RLS supports Executive and Regional Manager roles, and environment parameters separate server/database configuration from the model.

### 4. Agentic analytics layer

The FastAPI copilot accepts a natural-language business question. A transparent router selects one of four specialist domains: inventory, procurement, fulfillment, or sales. Each domain maps to a governed SQL query over validated analytics views.

The important design choice is that the agent is evidence-first. The SQL layer computes the numbers; the service exposes the evidence rows and then creates the concise explanation. Arbitrary write SQL is rejected.

A separate exception monitor runs the inventory, procurement, and fulfillment tools together so an operations user can quickly see the highest-priority exceptions.

### 5. Validation

Repository validators audit the Power BI project and all 14 pages. Agent regression tests cover routing, route-only service behavior, golden business questions, and FastAPI acceptance behavior. GitHub Actions runs these checks on pull requests.

The live local runtime was also validated against WideWorldImportersDW for inventory, procurement, fulfillment, sales, and the combined exception monitor.

## 10-minute technical deep dive

### SQL and semantic model

Start with the SQL analytics views and explain why business logic is centralized there. Then show the fact tables and conformed dimensions. Explain that explicit DAX measures sit on top of this model instead of embedding business logic independently in visuals.

### Power BI engineering

Show PBIP/PBIR/TMDL source control, parameterized data sources, RLS metadata, incremental-refresh readiness, and the data-quality page. Explain that the dashboard is treated as an engineering project, not only as a collection of charts.

### Copilot request flow

Use this flow:

```text
Business question
    -> FastAPI /ask
    -> deterministic domain router
    -> allow-listed specialist tool
    -> validated analytics SQL view
    -> structured evidence
    -> concise answer
```

A useful demo question is:

```text
Which SKUs are understocked and need reorder?
```

Then show the returned domain, tool metadata, evidence rows, and answer. Repeat with a supplier or backorder question to demonstrate that routing changes the analytical tool rather than generating unrestricted SQL.

### Governance

The database helper permits SELECT/CTE execution only. Domain queries are predefined and the requested result limit is bounded. No credentials are stored in the repository. This keeps metric generation deterministic and auditable.

### Exception monitoring

Call the exception endpoint and explain that it aggregates operational exceptions across inventory, procurement, and fulfillment. This is the foundation for future scheduled alerts, but the current repository intentionally does not claim cloud scheduling or notification delivery.

### Testing and CI

Show the golden-question evaluation and API acceptance tests. Explain that CI does not require the local SQL Server because route-only API tests verify HTTP behavior independently, while live database acceptance is performed in the configured local environment.

## Live demo sequence

1. Open the Executive Overview and briefly show the 14-page report navigation.
2. Show the dimensional model and one governed SQL analytics view.
3. Start the FastAPI service.
4. Open the API documentation and call `GET /health`.
5. Ask an inventory question through `POST /ask` and point to the evidence rows.
6. Ask a procurement or fulfillment question and show the domain change.
7. Call `GET /exceptions` to show cross-domain operational triage.
8. Finish with the GitHub Actions checks and source-controlled PBIP project.

## Resume bullets

- Built an end-to-end supply-chain analytics platform on SQL Server and Power BI with a dimensional model, 113 DAX measures, dynamic RLS, environment parameterization, automated QA, and a 14-page operational report.
- Developed an evidence-first FastAPI analytics copilot that routes natural-language questions to governed inventory, procurement, fulfillment, and sales tools backed by validated read-only SQL views.
- Added cross-domain exception monitoring and CI regression coverage for routing, golden business questions, API behavior, PBIP/PBIR/TMDL structure, and report-page quality checks.

## Claims to avoid

Do not describe the project as a deployed production AI system, autonomous write agent, hosted LLM application, or real-time cloud alerting platform. Those are possible extensions, not features implemented in the repository today.
