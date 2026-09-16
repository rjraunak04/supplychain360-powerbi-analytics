# Changelog

All notable project changes are documented here.

## 1.0.0 — 2026-09-16

### Portfolio source release
- Completed 14-page supply-chain control tower
- 113 explicit DAX measures across inventory, procurement, fulfillment, sales, profitability and movement
- Added Product 360 and Supplier 360 entity views
- Added Data Quality & Model QA acceptance page
- Added SQL analytics installer and reconciliation layer
- Added DEV/TEST/PROD source parameterization
- Added dynamic Regional Manager RLS plus Executive role
- Added incremental-refresh range parameters/filters
- Added PBIP/PBIR/TMDL source control
- Added GitHub Actions quality gate
- Added Desktop-strict PBIR validation
- Added automated page-by-page semantic-reference audit for all 14 pages
- Repaired PBIR sort metadata that caused blank Desktop exploration
- Repaired profitability measures and fulfillment hotspot visual
- Added governance, testing, performance, deployment, monitoring, accessibility and recruiter documentation

### Final automated QA
- 14/14 registered pages PASS
- 300 report visuals represented in the PBIR source
- no registered blank report page
- no broken visual field/measure references
- no broken semantic relationship references
- no PBIX/PBIT binary committed
- page-specific regression gates enabled

### Optional deployment evidence
Power BI Service publication, gateway/scheduled refresh screenshots, runtime Performance Analyzer captures, and tenant-specific RLS evidence remain optional deployment extensions and are not required for the source portfolio release.


## Unreleased — Production & Recruiter Hardening

### Added
- Parameterized SQL Server/database/environment model settings
- RangeStart/RangeEnd incremental-refresh filters on growing fact tables
- Dynamic regional RLS with UPN-based access mapping
- Executive full-access semantic-model role
- GitHub Actions PBIP/PBIR/TMDL quality gate
- Static validator for report/model/SQL repository integrity
- Production deployment/gateway runbook
- Performance engineering runbook
- Accessibility and mobile readiness checklist
- Architecture decision records
- Recruiter/interview walkthrough
- Expanded recruiter-grade README
- Security and contribution policies

### Existing analytical solution
- 14 report pages
- 113 explicit DAX measures
- Five fact domains
- Conformed dimension model
- Product 360 and Supplier 360 views
- SQL analytics and reconciliation layer
- Inventory current-snapshot QA
- PBIP/PBIR/TMDL source control

### Pending runtime evidence
- Final local Refresh All screenshot
- Performance Analyzer evidence
- RLS View-as / Service evidence
- Power BI Service refresh-history evidence
- Mobile layout screenshot
