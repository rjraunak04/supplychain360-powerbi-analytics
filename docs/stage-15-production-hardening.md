# Stage 15 — Production & Recruiter Hardening

## Completed in source control

### Security
- Dynamic Regional Manager RLS using `USERPRINCIPALNAME()`
- Executive full-read role
- Hidden Security User Access mapping table
- Production SQL security-mapping template
- Security policy and OLS design guidance

### Environment management
- ServerName parameter
- DatabaseName parameter
- EnvironmentName parameter
- DEV / TEST / PROD configuration template

### Refresh scalability
- RangeStart and RangeEnd parameters
- date-window filters on growing transactional facts
- incremental-refresh production strategy

### CI/CD
- GitHub Actions static PBIP/PBIR/TMDL quality gate
- pull request QA template
- issue template
- source-release packaging workflow
- reproducible source ZIP packager
- Dependabot for GitHub Actions
- CODEOWNERS

### Quality and testing
- static project validator
- one-command Windows QA runner
- SQL reconciliation layer
- release gate checklist
- multi-layer testing strategy

### Production operations
- Power BI Service deployment runbook
- on-premises gateway guidance
- scheduled refresh guidance
- monitoring/SLA framework
- rollback/versioning guidance

### Performance
- model performance engineering checklist
- Performance Analyzer procedure
- performance budgets
- evidence capture plan

### Governance
- data lineage
- domain ownership model
- architecture decision records
- KPI governance
- change-control process

### UX / accessibility
- accessibility checklist
- consistent semantic color guidance
- mobile-layout strategy

### Recruiter presentation
- expanded recruiter-grade README
- 14-page catalog
- 112-measure engineering summary
- architecture Mermaid diagrams
- recruiter walkthrough
- job skill matrix
- screenshot/evidence checklist

## Runtime-only tasks

The following require an interactive Power BI Desktop/Service session and cannot be truthfully marked complete by GitHub static automation:

- successful local Refresh All on the newest model
- Power BI Desktop TMDL runtime parse validation
- Performance Analyzer timings
- View-as RLS evidence
- actual mobile layout saved from Desktop
- Power BI Service publication
- gateway mapping
- scheduled refresh success
- refresh-history screenshot
- final report screenshots

These tasks are tracked in GitHub Issue #1.

## Release rule

Do not tag `v1.0.0` until the runtime-only gates above that apply to the portfolio are completed.
