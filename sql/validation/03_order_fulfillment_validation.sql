USE WideWorldImportersDW;
GO

-- =====================================================
-- 1. Overall Order Fulfillment KPIs
-- =====================================================

SELECT
    COUNT(*) AS TotalOrderLines,
    COUNT(DISTINCT [WWI Order ID]) AS TotalOrders,
    SUM([Quantity]) AS TotalOrderedQuantity,

    SUM([Is Backordered]) AS BackorderedLines,

    CAST(
        100.0 * SUM([Is Backordered])
        / NULLIF(COUNT(*), 0)
        AS decimal(10,2)
    ) AS BackorderLinePercent

FROM analytics.vw_order_fulfillment;
GO


-- =====================================================
-- 2. Fulfillment Status Distribution
-- =====================================================

SELECT
    [Fulfillment Status],

    COUNT(*) AS OrderLines,

    SUM([Quantity]) AS TotalQuantity,

    SUM([Total Including Tax]) AS OrderValue

FROM analytics.vw_order_fulfillment

GROUP BY [Fulfillment Status]

ORDER BY OrderValue DESC;
GO


-- =====================================================
-- 3. Products With Highest Backorder Rate
-- =====================================================

SELECT TOP 20
    [Stock Item],

    COUNT(*) AS OrderLines,

    SUM([Quantity]) AS OrderedQuantity,

    SUM([Is Backordered]) AS BackorderedLines,

    CAST(
        100.0 * SUM([Is Backordered])
        / NULLIF(COUNT(*), 0)
        AS decimal(10,2)
    ) AS BackorderRatePercent

FROM analytics.vw_order_fulfillment

GROUP BY [Stock Item]

HAVING COUNT(*) >= 10

ORDER BY BackorderRatePercent DESC;
GO


-- =====================================================
-- 4. Data Quality Check
-- =====================================================

SELECT
    SUM(
        CASE
            WHEN [Customer Key] IS NULL THEN 1
            ELSE 0
        END
    ) AS MissingCustomerKeys,

    SUM(
        CASE
            WHEN [Stock Item Key] IS NULL THEN 1
            ELSE 0
        END
    ) AS MissingStockItemKeys

FROM analytics.vw_order_fulfillment;
GO
