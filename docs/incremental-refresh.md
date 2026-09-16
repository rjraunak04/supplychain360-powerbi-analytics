# Incremental Refresh Strategy

## Current implementation

The semantic model defines the reserved Power Query parameters:

- `RangeStart`
- `RangeEnd`

The large transactional facts use these parameters in their Power Query filters:

- Fact Order Fulfillment → Order Date Key
- Fact Procurement → Date Key
- Fact Sales Demand → Invoice Date Key
- Fact Stock Movement → Date Key

The current sample defaults span the full Wide World Importers history so local Desktop validation remains complete.

## Production policy recommendation

For a real continuously growing warehouse:

| Fact | Historical archive | Refresh window | Suggested granularity |
|---|---:|---:|---|
| Sales Demand | 5 years | 7 days | Day |
| Order Fulfillment | 3 years | 7 days | Day |
| Stock Movement | 3 years | 3 days | Day |
| Procurement | 3 years | 14 days | Day |

Inventory is a current-state snapshot and should normally use standard refresh rather than date-partition incremental refresh.

## Activation steps

1. Confirm the date filters fold back to SQL Server.
2. In Power BI Desktop, select each eligible fact table.
3. Configure Incremental Refresh using `RangeStart` and `RangeEnd`.
4. Publish to Power BI Service/Fabric.
5. Run the initial refresh.
6. Verify partition creation and refresh history.
7. Monitor duration and failures.

## Important rule

Use `>= RangeStart` and `< RangeEnd`, not inclusive boundaries on both sides, to avoid duplicate boundary rows across partitions.

## Acceptance criteria

- Query folding remains available after the date filter.
- Initial service refresh succeeds.
- Subsequent refresh reads only the intended recent window.
- Historical partitions remain stable.
- KPI totals reconcile with full-history SQL benchmarks.
