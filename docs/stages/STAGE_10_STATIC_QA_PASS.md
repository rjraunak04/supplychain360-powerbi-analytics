# Stage 10 Static QA — PASS

Static source validation completed on the PBIP/PBIR project.

Checks passed:
- PBIP report artifact points to SupplyChain360.Report
- Report datasetReference points to ../SupplyChain360.SemanticModel
- 5 report pages registered in pages.json
- Active page exists in page order
- All 117 report JSON files parse successfully
- All 5 page.json files exist
- All visual field and measure references resolve to semantic-model objects
- All relationship column references resolve
- Missing Days To Pick semantic-model column restored so Average Days to Pick is valid
- No remaining direct TMDL table/column references are unresolved

Runtime data refresh still depends on the local SQL Server instance at localhost / WideWorldImportersDW.
