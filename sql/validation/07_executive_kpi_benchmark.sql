USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- Executive KPI SQL Benchmark
-- ============================================================

SELECT

    -- ========================================================
    -- INVENTORY
    -- ========================================================

    (
        SELECT CAST(
            SUM([Inventory Value])
            AS decimal(18,2)
        )
        FROM analytics.vw_inventory
    ) AS TotalInventoryValue,


    (
        SELECT COUNT(*)
        FROM analytics.vw_inventory
        WHERE [Inventory Status] = 'Stockout'
    ) AS StockoutSKUs,


    (
        SELECT COUNT(*)
        FROM analytics.vw_inventory
        WHERE [Inventory Status] = 'Reorder Required'
    ) AS ReorderRequiredSKUs,


    (
        SELECT COUNT(*)
        FROM analytics.vw_inventory
        WHERE [Inventory Status] = 'Overstock'
    ) AS OverstockSKUs,


    -- ========================================================
    -- PROCUREMENT
    -- ========================================================

    (
        SELECT COUNT(DISTINCT [WWI Purchase Order ID])
        FROM analytics.vw_procurement
    ) AS PurchaseOrders,


    (
        SELECT CAST(
            100.0 * SUM([Received Quantity])
            / NULLIF(SUM([Ordered Quantity]), 0)
            AS decimal(10,2)
        )
        FROM analytics.vw_procurement
    ) AS ProcurementFulfillmentPercent,


    (
        SELECT SUM([Outstanding Quantity])
        FROM analytics.vw_procurement
    ) AS OutstandingPurchaseQuantity,


    -- ========================================================
    -- ORDER FULFILLMENT
    -- ========================================================

    (
        SELECT COUNT(DISTINCT [WWI Order ID])
        FROM analytics.vw_order_fulfillment
    ) AS TotalOrders,


    (
        SELECT CAST(
            100.0 * SUM([Is Backordered])
            / NULLIF(COUNT(*), 0)
            AS decimal(10,2)
        )
        FROM analytics.vw_order_fulfillment
    ) AS BackorderLinePercent,


    (
        SELECT COUNT(*)
        FROM analytics.vw_order_fulfillment
        WHERE [Fulfillment Status] = 'Pending Pick'
    ) AS PendingPickLines,


    (
        SELECT CAST(
            AVG(CAST([Days To Pick] AS decimal(10,2)))
            AS decimal(10,2)
        )
        FROM analytics.vw_order_fulfillment
        WHERE [Days To Pick] IS NOT NULL
    ) AS AverageDaysToPick,


    -- ========================================================
    -- SALES
    -- ========================================================

    (
        SELECT CAST(
            SUM([Total Excluding Tax])
            AS decimal(18,2)
        )
        FROM analytics.vw_sales_demand
    ) AS Revenue,


    (
        SELECT CAST(
            SUM([Profit])
            AS decimal(18,2)
        )
        FROM analytics.vw_sales_demand
    ) AS TotalProfit,


    (
        SELECT CAST(
            100.0 * SUM([Profit])
            / NULLIF(SUM([Total Excluding Tax]), 0)
            AS decimal(10,2)
        )
        FROM analytics.vw_sales_demand
    ) AS ProfitMarginPercent,


    (
        SELECT SUM([Quantity])
        FROM analytics.vw_sales_demand
    ) AS UnitsSold,


    (
        SELECT CAST(
            AVG(CAST([Delivery Days] AS decimal(10,2)))
            AS decimal(10,2)
        )
        FROM analytics.vw_sales_demand
        WHERE [Delivery Days] IS NOT NULL
    ) AS AverageDeliveryDays,


    -- ========================================================
    -- MOVEMENT
    -- ========================================================

    (
        SELECT SUM([Stock In Quantity])
        FROM analytics.vw_stock_movement
    ) AS TotalStockIn,


    (
        SELECT SUM([Stock Out Quantity])
        FROM analytics.vw_stock_movement
    ) AS TotalStockOut,


    (
        SELECT SUM([Quantity])
        FROM analytics.vw_stock_movement
    ) AS NetStockMovement;
GO
