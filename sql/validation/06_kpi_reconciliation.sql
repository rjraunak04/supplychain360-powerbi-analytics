USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- Raw-to-Analytics Reconciliation
-- ============================================================


-- ============================================================
-- 1. INVENTORY RECONCILIATION
-- ============================================================

SELECT
    'Inventory Row Count' AS CheckName,

    (SELECT COUNT(*)
     FROM Fact.[Stock Holding]) AS RawValue,

    (SELECT COUNT(*)
     FROM analytics.vw_inventory) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT COUNT(*) FROM Fact.[Stock Holding])
            =
            (SELECT COUNT(*) FROM analytics.vw_inventory)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


-- Inventory Quantity
SELECT
    'Inventory Quantity On Hand' AS CheckName,

    (SELECT SUM([Quantity On Hand])
     FROM Fact.[Stock Holding]) AS RawValue,

    (SELECT SUM([Quantity On Hand])
     FROM analytics.vw_inventory) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT SUM([Quantity On Hand])
             FROM Fact.[Stock Holding])
            =
            (SELECT SUM([Quantity On Hand])
             FROM analytics.vw_inventory)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


-- ============================================================
-- 2. PROCUREMENT RECONCILIATION
-- ============================================================

SELECT
    'Procurement Row Count' AS CheckName,

    (SELECT COUNT(*)
     FROM Fact.[Purchase]) AS RawValue,

    (SELECT COUNT(*)
     FROM analytics.vw_procurement) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT COUNT(*) FROM Fact.[Purchase])
            =
            (SELECT COUNT(*) FROM analytics.vw_procurement)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


SELECT
    'Procurement Ordered Quantity' AS CheckName,

    (SELECT SUM([Ordered Quantity])
     FROM Fact.[Purchase]) AS RawValue,

    (SELECT SUM([Ordered Quantity])
     FROM analytics.vw_procurement) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT SUM([Ordered Quantity])
             FROM Fact.[Purchase])
            =
            (SELECT SUM([Ordered Quantity])
             FROM analytics.vw_procurement)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


-- ============================================================
-- 3. ORDER RECONCILIATION
-- ============================================================

SELECT
    'Order Row Count' AS CheckName,

    (SELECT COUNT(*)
     FROM Fact.[Order]) AS RawValue,

    (SELECT COUNT(*)
     FROM analytics.vw_order_fulfillment) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT COUNT(*) FROM Fact.[Order])
            =
            (SELECT COUNT(*)
             FROM analytics.vw_order_fulfillment)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


SELECT
    'Order Value' AS CheckName,

    (SELECT SUM([Total Including Tax])
     FROM Fact.[Order]) AS RawValue,

    (SELECT SUM([Total Including Tax])
     FROM analytics.vw_order_fulfillment) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT SUM([Total Including Tax])
             FROM Fact.[Order])
            =
            (SELECT SUM([Total Including Tax])
             FROM analytics.vw_order_fulfillment)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


-- ============================================================
-- 4. SALES RECONCILIATION
-- ============================================================

SELECT
    'Sales Row Count' AS CheckName,

    (SELECT COUNT(*)
     FROM Fact.[Sale]) AS RawValue,

    (SELECT COUNT(*)
     FROM analytics.vw_sales_demand) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT COUNT(*) FROM Fact.[Sale])
            =
            (SELECT COUNT(*) FROM analytics.vw_sales_demand)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


SELECT
    'Sales Revenue' AS CheckName,

    (SELECT SUM([Total Excluding Tax])
     FROM Fact.[Sale]) AS RawValue,

    (SELECT SUM([Total Excluding Tax])
     FROM analytics.vw_sales_demand) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT SUM([Total Excluding Tax])
             FROM Fact.[Sale])
            =
            (SELECT SUM([Total Excluding Tax])
             FROM analytics.vw_sales_demand)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


SELECT
    'Sales Profit' AS CheckName,

    (SELECT SUM([Profit])
     FROM Fact.[Sale]) AS RawValue,

    (SELECT SUM([Profit])
     FROM analytics.vw_sales_demand) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT SUM([Profit])
             FROM Fact.[Sale])
            =
            (SELECT SUM([Profit])
             FROM analytics.vw_sales_demand)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


-- ============================================================
-- 5. STOCK MOVEMENT RECONCILIATION
-- ============================================================

SELECT
    'Movement Row Count' AS CheckName,

    (SELECT COUNT(*)
     FROM Fact.[Movement]) AS RawValue,

    (SELECT COUNT(*)
     FROM analytics.vw_stock_movement) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT COUNT(*) FROM Fact.[Movement])
            =
            (SELECT COUNT(*) FROM analytics.vw_stock_movement)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO


SELECT
    'Net Stock Movement' AS CheckName,

    (SELECT SUM([Quantity])
     FROM Fact.[Movement]) AS RawValue,

    (SELECT SUM([Quantity])
     FROM analytics.vw_stock_movement) AS AnalyticsValue,

    CASE
        WHEN
            (SELECT SUM([Quantity])
             FROM Fact.[Movement])
            =
            (SELECT SUM([Quantity])
             FROM analytics.vw_stock_movement)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS TestStatus;
GO
