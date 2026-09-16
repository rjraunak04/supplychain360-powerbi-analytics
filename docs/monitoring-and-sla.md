# Monitoring & Operational SLA

## Objective

A production BI solution requires monitoring after deployment, not only successful publication.

## Refresh monitoring

Track:
- last successful refresh time
- last failed refresh time
- refresh duration
- gateway availability
- consecutive failures
- source connectivity failures
- credential expiry incidents

## Data freshness

The semantic model already exposes latest Sales, Order and Movement dates on the QA page.

Recommended service-level targets for a daily-refresh implementation:

| Area | Target |
|---|---|
| Scheduled refresh success | >= 99% |
| Data available | before agreed business start time |
| Consecutive refresh failures | 0 tolerated without alert |
| Critical KPI reconciliation failure | block release |
| Gateway offline | investigate immediately |

Targets should be adapted to the actual business SLA; they are portfolio examples, not universal standards.

## Alerting pattern

In an enterprise implementation:
1. Power BI/Fabric refresh failure generates platform notification.
2. Support owner checks gateway/source status.
3. Failed release/refresh is logged.
4. Repeated failures escalate to data-platform owner.
5. KPI reconciliation issues block publication.

## Operational runbook

For a refresh failure:
1. Check SQL Server/gateway availability.
2. Confirm server/database parameters.
3. Validate credentials.
4. Check whether SQL Server is accidentally in single-user mode.
5. Run local static QA.
6. Test source query in Power Query/SSMS.
7. Retry on-demand refresh.
8. Document the root cause.

## Release monitoring evidence

For portfolio publication, capture a sanitized successful refresh-history screenshot after Power BI Service deployment.
