USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- View: analytics.vw_order_fulfillment
-- Purpose:
--   Analyze customer orders, picking performance,
--   backorders and fulfillment bottlenecks.
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

CREATE OR ALTER VIEW analytics.vw_order_fulfillment
AS

SELECT
    -- Keys
    o.[Order Key],
    o.[City Key],
    o.[Customer Key],
    o.[Stock Item Key],
    o.[Salesperson Key],
    o.[Picker Key],

    -- Dates
    o.[Order Date Key],
    o.[Picked Date Key],

    -- Business identifiers
    o.[WWI Order ID],
    o.[WWI Backorder ID],

    -- Customer attributes
    c.[Customer],
    c.[Category] AS [Customer Category],
    c.[Buying Group],

    -- Product attributes
    si.[Stock Item],
    si.[Brand],

    -- Order-line attributes
    o.[Description],
    o.[Package],
    o.[Quantity],
    o.[Unit Price],
    o.[Tax Rate],
    o.[Total Excluding Tax],
    o.[Tax Amount],
    o.[Total Including Tax],

    -- --------------------------------------------------------
    -- Fulfillment metrics
    -- --------------------------------------------------------

    CASE
        WHEN o.[WWI Backorder ID] IS NOT NULL
            THEN 1
        ELSE 0
    END AS [Is Backordered],

    CASE
        WHEN o.[WWI Backorder ID] IS NOT NULL
            THEN o.[Quantity]
        ELSE 0
    END AS [Backordered Quantity],

    CASE
        WHEN o.[Picked Date Key] IS NOT NULL
            THEN 1
        ELSE 0
    END AS [Is Picked],

    CASE
        WHEN o.[Picked Date Key] IS NOT NULL
        THEN DATEDIFF(
            DAY,
            o.[Order Date Key],
            o.[Picked Date Key]
        )
        ELSE NULL
    END AS [Days To Pick],

    CASE
        WHEN o.[WWI Backorder ID] IS NOT NULL
            THEN 'Backordered'

        WHEN o.[Picked Date Key] IS NULL
            THEN 'Pending Pick'

        ELSE 'Picked'
    END AS [Fulfillment Status],

    CASE
        WHEN o.[Picked Date Key] IS NULL
            THEN 'Not Completed'

        WHEN DATEDIFF(
            DAY,
            o.[Order Date Key],
            o.[Picked Date Key]
        ) = 0
            THEN 'Same Day'

        WHEN DATEDIFF(
            DAY,
            o.[Order Date Key],
            o.[Picked Date Key]
        ) = 1
            THEN 'Next Day'

        ELSE '2+ Days'
    END AS [Picking Speed Category]

FROM Fact.[Order] AS o

LEFT JOIN Dimension.[Customer] AS c
    ON o.[Customer Key] = c.[Customer Key]

LEFT JOIN Dimension.[Stock Item] AS si
    ON o.[Stock Item Key] = si.[Stock Item Key];
GO
