USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- View: analytics.vw_procurement
-- Purpose:
--   Procurement and supplier fulfillment analytics layer.
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

CREATE OR ALTER VIEW analytics.vw_procurement
AS

SELECT
    -- Keys
    p.[Purchase Key],
    p.[Date Key],
    p.[Supplier Key],
    p.[Stock Item Key],

    -- Purchase identifiers
    p.[WWI Purchase Order ID],

    -- Supplier details
    s.[Supplier],
    s.[Category] AS [Supplier Category],
    s.[Primary Contact] AS [Supplier Primary Contact],
    s.[Payment Days],

    -- Product details
    si.[Stock Item],
    si.[Brand],
    si.[Buying Package],
    si.[Lead Time Days],
    si.[Quantity Per Outer],

    -- Purchase quantities
    p.[Ordered Outers],
    p.[Ordered Quantity],
    p.[Received Outers],
    p.[Package],
    p.[Is Order Finalized],

    -- --------------------------------------------------------
    -- Derived metrics
    -- --------------------------------------------------------

    p.[Received Outers] * si.[Quantity Per Outer]
        AS [Received Quantity],

    CASE
        WHEN
            p.[Ordered Quantity]
            >
            (p.[Received Outers] * si.[Quantity Per Outer])

        THEN
            p.[Ordered Quantity]
            -
            (p.[Received Outers] * si.[Quantity Per Outer])

        ELSE 0
    END AS [Outstanding Quantity],

    (
        p.[Received Outers] * si.[Quantity Per Outer]
    ) - p.[Ordered Quantity]
        AS [Receipt Quantity Variance],

    CAST(
        100.0
        * (p.[Received Outers] * si.[Quantity Per Outer])
        / NULLIF(p.[Ordered Quantity], 0)
        AS decimal(10,2)
    ) AS [Receipt Fulfillment Percent],

    CASE
        WHEN p.[Received Outers] = 0
            THEN 'Not Received'

        WHEN
            (p.[Received Outers] * si.[Quantity Per Outer])
            < p.[Ordered Quantity]
            THEN 'Partially Received'

        WHEN
            (p.[Received Outers] * si.[Quantity Per Outer])
            >= p.[Ordered Quantity]
            THEN 'Fully Received'

        ELSE 'Unknown'
    END AS [Receipt Status],

    CASE
        WHEN p.[Is Order Finalized] = 1
            THEN 'Finalized'
        ELSE 'Open'
    END AS [Purchase Order Status]

FROM Fact.[Purchase] AS p

LEFT JOIN Dimension.[Supplier] AS s
    ON p.[Supplier Key] = s.[Supplier Key]

LEFT JOIN Dimension.[Stock Item] AS si
    ON p.[Stock Item Key] = si.[Stock Item Key];
GO
