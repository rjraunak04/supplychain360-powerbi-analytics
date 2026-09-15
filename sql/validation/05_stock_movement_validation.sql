USE WideWorldImportersDW;
GO

-- ============================================================
-- 1. Overall Stock Movement
-- ============================================================

SELECT
    COUNT(*) AS MovementRows,

    SUM([Stock In Quantity]) AS TotalStockIn,

    SUM([Stock Out Quantity]) AS TotalStockOut,

    SUM([Quantity]) AS NetStockMovement

FROM analytics.vw_stock_movement;
GO


-- ============================================================
-- 2. Flow Direction Distribution
-- ============================================================

SELECT
    [Flow Direction],
    COUNT(*) AS MovementRows,
    SUM([Absolute Movement Quantity]) AS MovementQuantity

FROM analytics.vw_stock_movement

GROUP BY [Flow Direction]

ORDER BY MovementQuantity DESC;
GO


-- ============================================================
-- 3. Movement by Transaction Type
-- ============================================================

SELECT
    [Transaction Type],
    COUNT(*) AS MovementRows,
    SUM([Stock In Quantity]) AS StockIn,
    SUM([Stock Out Quantity]) AS StockOut

FROM analytics.vw_stock_movement

GROUP BY [Transaction Type]

ORDER BY MovementRows DESC;
GO


-- ============================================================
-- 4. Data Quality
-- ============================================================

SELECT
    SUM(
        CASE
            WHEN [Stock Item Key] IS NULL THEN 1
            ELSE 0
        END
    ) AS MissingStockItemKeys,

    SUM(
        CASE
            WHEN [Transaction Type Key] IS NULL THEN 1
            ELSE 0
        END
    ) AS MissingTransactionTypeKeys

FROM analytics.vw_stock_movement;
GO
