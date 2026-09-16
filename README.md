# SupplyChain360 — Enterprise Power BI Supply Chain Control Tower

SupplyChain360 is an end-to-end supply-chain analytics portfolio project built on Microsoft Wide World Importers DW using SQL Server, Power Query, dimensional modeling, DAX, PBIP/PBIR and Power BI.

## Final dashboard coverage

The final PBIP contains 14 pages covering executive KPIs, inventory, procurement, fulfillment, sales, profitability, stock movement, Product 360, Supplier 360 and model QA.

## Architecture

SQL Server / WideWorldImportersDW → Power Query → Star Schema → DAX → PBIR dashboards → Power BI Service.

## Refresh hardening

Fact Order Fulfillment now sources `Fact.Order` directly and derives `Days To Pick`, `Is Backordered`, `Backordered Quantity`, `Is Picked`, `Fulfillment Status` and `Picking Speed Category` in Power Query. This removes the local refresh failure caused by a stale `analytics.vw_order_fulfillment` schema missing `Days To Pick`.

## Quality gates

Static QA passed with 14 registered report pages, zero JSON parse errors, zero broken visual field/measure references, zero broken relationship references and zero broken direct DAX table/column references.

Runtime validation still requires a successful local refresh against `localhost / WideWorldImportersDW`.
