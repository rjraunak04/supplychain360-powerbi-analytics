USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- View: analytics.vw_inventory
-- Purpose:
--   Business-ready inventory layer for stock health,
--   replenishment and inventory-value analysis.
-- ============================================================

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'analytics'
)
BEGIN
    EXEC('CREATE SCHEMA analytics');
END;
GO

CREATE OR ALTER VIEW analytics.vw_inventory
AS

SELECT
    -- Keys
    sh.[Stock Holding Key],
    sh.[Stock Item Key],

    -- Product attributes
    si.[Stock Item],
    si.[Brand],
    si.[Color],
    si.[Size],
    si.[Buying Package],
    si.[Selling Package],
    si.[Lead Time Days],
    si.[Quantity Per Outer],
    si.[Is Chiller Stock],
    si.[Unit Price],
    si.[Recommended Retail Price],

    -- Inventory attributes
    sh.[Quantity On Hand],
    sh.[Bin Location],
    sh.[Last Stocktake Quantity],
    sh.[Last Cost Price],
    sh.[Reorder Level],
    sh.[Target Stock Level],

    -- --------------------------------------------------------
    -- Derived business metrics
    -- --------------------------------------------------------

    CAST(
        sh.[Quantity On Hand] * sh.[Last Cost Price]
        AS decimal(18,2)
    ) AS [Inventory Value],

    sh.[Quantity On Hand] - sh.[Reorder Level]
        AS [Stock Above Reorder Level],

    sh.[Target Stock Level] - sh.[Quantity On Hand]
        AS [Gap To Target],

    CASE
        WHEN sh.[Quantity On Hand] <= 0
            THEN 1
        ELSE 0
    END AS [Is Stockout],

    CASE
        WHEN sh.[Quantity On Hand] <= sh.[Reorder Level]
            THEN 1
        ELSE 0
    END AS [Needs Reorder],

    CASE
        WHEN sh.[Quantity On Hand] > sh.[Target Stock Level]
            THEN 1
        ELSE 0
    END AS [Is Overstock],

    CASE
        WHEN sh.[Quantity On Hand] <= 0
            THEN 'Stockout'

        WHEN sh.[Quantity On Hand] <= sh.[Reorder Level]
            THEN 'Reorder Required'

        WHEN sh.[Quantity On Hand] > sh.[Target Stock Level]
            THEN 'Overstock'

        ELSE 'Healthy'
    END AS [Inventory Status],

    CASE
        WHEN sh.[Target Stock Level] > sh.[Quantity On Hand]
        THEN sh.[Target Stock Level] - sh.[Quantity On Hand]
        ELSE 0
    END AS [Suggested Reorder Quantity]

FROM Fact.[Stock Holding] AS sh

LEFT JOIN Dimension.[Stock Item] AS si
    ON sh.[Stock Item Key] = si.[Stock Item Key];
GO
