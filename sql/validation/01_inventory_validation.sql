USE WideWorldImportersDW;
GO

-- =====================================================
-- 1. Inventory Overview
-- =====================================================

SELECT
    COUNT(*) AS TotalStockItems,

    SUM([Quantity On Hand]) AS TotalQuantityOnHand,

    CAST(
        SUM([Inventory Value])
        AS decimal(18,2)
    ) AS TotalInventoryValue

FROM analytics.vw_inventory;
GO


-- =====================================================
-- 2. Inventory Status Distribution
-- =====================================================

SELECT
    [Inventory Status],

    COUNT(*) AS ProductCount,

    SUM([Quantity On Hand]) AS TotalQuantity,

    CAST(
        SUM([Inventory Value])
        AS decimal(18,2)
    ) AS InventoryValue

FROM analytics.vw_inventory

GROUP BY [Inventory Status]

ORDER BY InventoryValue DESC;
GO


-- =====================================================
-- 3. Stock Items Below Reorder Level
-- =====================================================

SELECT
    [Stock Item Key],
    [Stock Item],
    [Quantity On Hand],
    [Reorder Level],
    [Target Stock Level],
    [Gap To Target],
    [Inventory Value]

FROM analytics.vw_inventory

WHERE [Quantity On Hand] <= [Reorder Level]

ORDER BY [Gap To Target] DESC;
GO


-- =====================================================
-- 4. Uniqueness Check
-- =====================================================

SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT [Stock Item Key]) AS UniqueStockItems

FROM analytics.vw_inventory;
GO
