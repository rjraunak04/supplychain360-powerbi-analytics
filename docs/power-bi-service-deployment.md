# Power BI Service Deployment Runbook

## Target lifecycle

`DEV → TEST → PROD`

The repository stores PBIP/PBIR/TMDL source. Deployment credentials and tenant-specific identifiers must remain outside Git.

## Publish checklist

1. Run `python scripts/validate_powerbi_project.py`.
2. Open `powerbi/SupplyChain360.pbip` in Power BI Desktop.
3. Run **Refresh All**.
4. Confirm Data Quality & Model QA = PASS.
5. Validate RLS with **View as**.
6. Record Performance Analyzer baseline.
7. Save the project.
8. Publish to the target Power BI workspace.

## Gateway for local SQL Server

Because the sample source is SQL Server on `localhost`, Power BI Service requires an on-premises data gateway (or a reachable enterprise SQL endpoint).

Production steps:

- Install/configure the standard on-premises data gateway on an always-on machine.
- Add a SQL Server data source.
- Map the semantic model to the gateway data source.
- Configure approved credentials.
- Test the connection.
- Trigger an on-demand refresh.
- Enable scheduled refresh after the manual refresh succeeds.

## Scheduled refresh

Suggested demo cadence:
- Daily during portfolio/demo use

Real production cadence should be aligned to source-system latency and business requirements.

## Deployment pipeline

For organizations with Fabric/Power BI deployment pipelines:

- DEV workspace: authoring and developer validation
- TEST workspace: UAT, RLS validation, reconciliation
- PROD workspace: controlled release

Change environment parameters during deployment rather than editing M queries.

## Post-deployment validation

- Refresh history shows success.
- RLS roles are populated and tested.
- Scheduled refresh is configured.
- Report links open for Viewer users.
- No workspace permission unintentionally bypasses the security design.
- Mobile layout/accessibility checks are completed.
- Release tag/change log updated.

## Evidence for portfolio

After publication, add:
- workspace/report screenshot with sensitive tenant details cropped
- successful refresh-history screenshot
- RLS test screenshot
- deployment architecture diagram
