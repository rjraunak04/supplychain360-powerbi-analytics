USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- View: analytics.vw_stock_movement
-- Purpose:
--   Inventory movement and stock-flow analytics layer.
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

CREATE OR ALTER VIEW analytics.vw_stock_movement
AS

SELECT
    -- Keys
    m.[Movement Key],
    m.[Date Key],
    m.[Stock Item Key],
    m.[Customer Key],
    m.[Supplier Key],
    m.[Transaction Type Key],

    -- Business identifiers
    m.[WWI Stock Item Transaction ID],
    m.[WWI Invoice ID],
    m.[WWI Purchase Order ID],

    -- Product
    si.[Stock Item],
    si.[Brand],
    si.[Color],
    si.[Size],
    si.[Is Chiller Stock],

    -- Transaction
    tt.[Transaction Type],

    -- Supplier / Customer
    s.[Supplier],
    c.[Customer],

    -- Core movement
    m.[Quantity],

    ABS(m.[Quantity]) AS [Absolute Movement Quantity],

    CASE
        WHEN m.[Quantity] > 0 THEN 'Stock In'
        WHEN m.[Quantity] < 0 THEN 'Stock Out'
        ELSE 'No Movement'
    END AS [Flow Direction],

    CASE
        WHEN m.[Quantity] > 0 THEN m.[Quantity]
        ELSE 0
    END AS [Stock In Quantity],

    CASE
        WHEN m.[Quantity] < 0 THEN ABS(m.[Quantity])
        ELSE 0
    END AS [Stock Out Quantity],

    CASE
        WHEN m.[Supplier Key] IS NOT NULL
             AND m.[WWI Purchase Order ID] IS NOT NULL
            THEN 'Procurement'

        WHEN m.[Customer Key] IS NOT NULL
             AND m.[WWI Invoice ID] IS NOT NULL
            THEN 'Customer Fulfillment'

        ELSE 'Other'
    END AS [Movement Source]

FROM Fact.[Movement] AS m

LEFT JOIN Dimension.[Stock Item] AS si
    ON m.[Stock Item Key] = si.[Stock Item Key]

LEFT JOIN Dimension.[Transaction Type] AS tt
    ON m.[Transaction Type Key] = tt.[Transaction Type Key]

LEFT JOIN Dimension.[Supplier] AS s
    ON m.[Supplier Key] = s.[Supplier Key]

LEFT JOIN Dimension.[Customer] AS c
    ON m.[Customer Key] = c.[Customer Key];
GO
