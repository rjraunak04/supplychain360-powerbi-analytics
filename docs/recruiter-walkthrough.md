# Recruiter / Interview Walkthrough

## 30-second summary

SupplyChain360 is an end-to-end Power BI supply-chain control tower built on SQL Server. It covers inventory, procurement, supplier performance, fulfillment, sales, profitability and stock movement using a star-schema semantic model, advanced DAX, PBIP/PBIR source control, automated static QA, dynamic RLS and deployment-ready environment parameters.

## 3-minute demo sequence

### 1. Executive Overview
Explain:
- headline supply-chain health
- revenue/profit trend
- inventory risk
- backorder rate
- supplier/procurement context

### 2. Inventory Intelligence
Show:
- stockouts/reorder/excess inventory
- inventory-value concentration
- replenishment priority
- SKU risk register

### 3. Procurement & Supplier Performance
Show:
- ordered vs received
- outstanding quantity
- supplier exposure
- procurement exceptions

### 4. Fulfillment & Backorders
Show:
- backorder rate
- pick performance
- customer/product hotspots

### 5. Product 360 / Supplier 360
Explain how conformed dimensions allow one entity to be analyzed across multiple fact domains.

### 6. Model + Engineering
Show:
- star schema
- centralized measure table
- role-playing relationships
- dynamic RLS
- parameterized environments
- GitHub Actions quality gate
- SQL validation scripts

## Technical discussion points

Be ready to explain:

- Why a star schema was preferred over a flat model
- Why facts are not directly related to other facts
- Why explicit measures are centralized
- When `USERELATIONSHIP()` is used
- Difference between SQL-derived row logic and DAX aggregation logic
- How inventory SCD duplication was prevented
- Why PBIP/PBIR/TMDL is better for Git than PBIX
- How dynamic RLS works
- How RangeStart/RangeEnd support incremental-refresh readiness
- How the CI script detects broken project metadata
- How the report would move from DEV to TEST to PROD

## Resume-ready project statement

**SupplyChain360 — Enterprise Supply Chain Analytics Control Tower**  
Built an end-to-end Power BI analytics platform on SQL Server/Wide World Importers using SQL analytics views, Power Query, star-schema modeling, 80+ DAX measures, dynamic RLS, PBIP/PBIR/TMDL source control and automated GitHub Actions validation; delivered 14 decision-support pages spanning inventory, procurement, fulfillment, sales, profitability, stock movement and entity-level 360 views.

Adjust the measure count in the resume only if the current repository count is revalidated.
