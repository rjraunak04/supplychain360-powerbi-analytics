USE WideWorldImportersDW;
GO

-- SupplyChain360 analytics-layer readiness check

WITH RequiredViews AS (
    SELECT 'vw_inventory' AS ViewName UNION ALL
    SELECT 'vw_procurement' UNION ALL
    SELECT 'vw_order_fulfillment' UNION ALL
    SELECT 'vw_sales_demand' UNION ALL
    SELECT 'vw_stock_movement'
)
SELECT
    r.ViewName,
    CASE WHEN v.object_id IS NULL THEN 'MISSING' ELSE 'READY' END AS Status
FROM RequiredViews r
LEFT JOIN sys.views v
    ON v.name = r.ViewName
LEFT JOIN sys.schemas s
    ON v.schema_id = s.schema_id
   AND s.name = 'analytics'
ORDER BY r.ViewName;
GO

IF OBJECT_ID('analytics.vw_procurement','V') IS NOT NULL
    SELECT TOP (1) * FROM analytics.vw_procurement;
GO

IF OBJECT_ID('analytics.vw_sales_demand','V') IS NOT NULL
    SELECT TOP (1) * FROM analytics.vw_sales_demand;
GO

IF OBJECT_ID('analytics.vw_stock_movement','V') IS NOT NULL
    SELECT TOP (1) * FROM analytics.vw_stock_movement;
GO
