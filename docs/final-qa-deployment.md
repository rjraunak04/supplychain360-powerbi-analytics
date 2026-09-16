# Final QA and Deployment

## Static QA
- Report JSON parse errors: 0
- Broken visual field / measure references: 0
- Broken relationship references: 0
- Broken direct DAX table / column references: 0
- Pages registered: 14

## Local runtime acceptance
1. Open `SupplyChain360.pbip`.
2. Confirm SQL Server is in multi-user mode.
3. Refresh against `localhost / WideWorldImportersDW`.
4. Confirm page `14 Data Quality & Model QA` loads.
5. Confirm `Inventory QA Status = PASS` and `Inventory Key QA = 0`.
6. Spot-check executive KPIs against SQL benchmark queries.

## Deployment
After runtime acceptance, publish to Power BI Service. For scheduled refresh of a local SQL Server source, configure the appropriate on-premises data gateway and credentials.
