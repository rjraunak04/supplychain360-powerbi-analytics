# Data Governance & Lineage

## Lineage

```mermaid
flowchart LR
  A[WideWorldImportersDW] --> B[SQL analytics views]
  B --> C[Power Query / M]
  C --> D[Semantic model / TMDL]
  D --> E[DAX measure layer]
  E --> F[PBIR reports]
  F --> G[Power BI Service / Fabric]
```

## Data-domain ownership

| Domain | Primary fact | Typical business owner |
|---|---|---|
| Inventory | Fact Inventory | Warehouse / Inventory Operations |
| Procurement | Fact Procurement | Procurement / Supply |
| Fulfillment | Fact Order Fulfillment | Logistics / Customer Operations |
| Sales | Fact Sales Demand | Commercial / Sales |
| Stock movement | Fact Stock Movement | Warehouse / Operations |

## Governance principles

- Keep business definitions in the KPI dictionary.
- Keep reusable source logic in governed SQL views.
- Treat the semantic model as a certified analytical contract.
- Store DAX measures centrally.
- Maintain one definition per KPI.
- Document inactive relationship usage.
- Keep technical keys hidden from consumers.
- Separate DEV, TEST and PROD parameter values.
- Never commit production credentials or personal security mappings.
- Reconcile high-impact KPIs against SQL before release.

## Change ownership

Changes to KPI definitions should update:
1. SQL validation, if source-side logic changes.
2. DAX measure implementation.
3. KPI dictionary.
4. Affected report visuals.
5. QA/reconciliation evidence.
6. Changelog.

## Data classification

The public/portfolio dataset is synthetic Microsoft sample data. If this architecture is reused for real data, classify columns such as customer contact data, employee data and user-security mappings before publication.

## Lineage acceptance

A reviewer should be able to trace any headline KPI from:
Report visual → DAX measure → semantic column → Power Query source → SQL view/source table.
