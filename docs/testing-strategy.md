# Testing Strategy

SupplyChain360 uses multiple testing layers rather than relying only on visual inspection.

## 1. Source and SQL tests

Located under `sql/validation/`.

Validate:
- source row counts
- uniqueness at expected grain
- KPI reconciliation
- inventory current-snapshot rules
- procurement, fulfillment, sales and movement logic

## 2. Semantic-model static tests

Run:

```bash
python scripts/validate_powerbi_project.py
```

The quality gate checks:
- required PBIP/PBIR/TMDL assets
- report JSON parsing
- registered pages
- table/relationship references
- source parameterization
- RLS metadata
- incremental-range filters
- accidental PBIX/PBIT binaries
- SQL view/validation coverage
- minimum measure-layer coverage

## 3. CI tests

GitHub Actions executes the static quality gate on:
- pushes to main
- pull requests targeting main

A failing quality gate should block a production release.

## 4. Runtime Power BI tests

After opening the PBIP:
- Refresh All succeeds
- no query errors
- no broken visual fields
- Data Quality & Model QA page passes
- KPI totals reconcile with SQL
- slicers cross-filter expected visuals
- inactive-date measures behave correctly
- drill-through/360 pages preserve context

## 5. Security tests

- Executive sees all data
- Regional Manager sees only mapped states
- unmapped regional user sees no regional data
- test with real Viewer identities in Service

## 6. Performance tests

Use Performance Analyzer and record:
- total page load
- slowest visuals
- DAX query time
- regressions after model changes

## Definition of Done

A release is complete only when static CI, local refresh, KPI reconciliation, RLS, and core page interaction tests pass.
