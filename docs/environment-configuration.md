# Environment Configuration

SupplyChain360 no longer hard-codes the SQL Server connection inside individual table queries.

## Semantic-model parameters

| Parameter | Default | Purpose |
|---|---|---|
| `ServerName` | `localhost` | SQL Server host / instance |
| `DatabaseName` | `WideWorldImportersDW` | Source database |
| `EnvironmentName` | `DEV` | Human-readable deployment environment |
| `RangeStart` | 2013-01-01 | Incremental-refresh lower bound |
| `RangeEnd` | 2017-01-01 | Incremental-refresh upper bound |

All SQL-backed table partitions reference `ServerName` and `DatabaseName`.

## Recommended environment mapping

| Environment | ServerName | DatabaseName |
|---|---|---|
| DEV | localhost | WideWorldImportersDW |
| TEST | test-sql-host | WideWorldImportersDW |
| PROD | prod-sql-host | WideWorldImportersDW |

Do not commit real production infrastructure values if the repository is public. Configure them in Power BI/Fabric deployment settings or approved environment-management tooling.

## Deployment principle

The PBIP source is environment-neutral. Only parameter values and service credentials should change between DEV, TEST and PROD.

This separation prevents developers from editing M code simply to move a report between environments.
