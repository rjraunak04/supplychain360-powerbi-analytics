# Recruiter Skill Matrix

This document maps common BI / Data Analyst / Power BI Developer requirements to concrete artifacts in SupplyChain360.

| Industry requirement | Evidence in project |
|---|---|
| SQL / T-SQL | `sql/views/`, `sql/validation/` |
| Data cleaning / transformation | Power Query M in TMDL partitions |
| Dimensional modeling | 5 fact domains + conformed dimensions |
| Star schema | `docs/data-model.md`, semantic relationships |
| DAX | 112 explicit measures in `_Measures.tmdl` |
| Time intelligence | YTD, LY, YoY and role-playing date measures |
| KPI design | `docs/kpi-dictionary.md` |
| Inventory analytics | pages 02–03 |
| Procurement / supplier analytics | pages 04–05 and Supplier 360 |
| Fulfillment / logistics | pages 06–07 |
| Sales / profitability | pages 08–09 |
| Operational stock movement | pages 10–11 |
| Drill / entity analysis | Product 360 and Supplier 360 |
| Data quality | page 14 + SQL reconciliation |
| RLS | Executive + dynamic Regional Manager roles |
| Power BI source control | PBIP/PBIR/TMDL |
| Git / GitHub | structured commits, PR/issue templates |
| CI validation | GitHub Actions quality gate |
| DEV/TEST/PROD readiness | parameterized ServerName/DatabaseName/EnvironmentName |
| Incremental refresh readiness | RangeStart/RangeEnd filters |
| Gateway / Service deployment | deployment runbook |
| Performance tuning | Performance Analyzer runbook and budgets |
| Governance / lineage | governance and architecture docs |
| Accessibility / mobile | accessibility/mobile checklist |
| Release management | changelog, release checklist, packaging workflow |

## Best roles to discuss this project for

- Power BI Developer
- BI Developer / BI Analyst
- Data Analyst
- Business Intelligence Analyst
- Analytics Engineer (junior / entry)
- Data Scientist roles where strong BI/business analytics is useful

## Interview positioning

Do not present the project as “14 dashboards.” Present it as:

> A version-controlled supply-chain semantic model and decision-support application with SQL validation, governed KPI definitions, dynamic security, automated static QA and a production deployment path.

That framing demonstrates engineering ownership rather than only visual design.
