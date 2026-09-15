USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- View: analytics.vw_sales_demand
-- Purpose:
--   Sales, demand, profitability and delivery-performance layer
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

CREATE OR ALTER VIEW analytics.vw_sales_demand
AS

SELECT
    -- ========================================================
    -- Keys
    -- ========================================================

    s.[Sale Key],
    s.[City Key],
    s.[Customer Key],
    s.[Bill To Customer Key],
    s.[Stock Item Key],
    s.[Salesperson Key],

    -- ========================================================
    -- Dates
    -- ========================================================

    s.[Invoice Date Key],
    s.[Delivery Date Key],

    -- ========================================================
    -- Business identifiers
    -- ========================================================

    s.[WWI Invoice ID],

    -- ========================================================
    -- Customer attributes
    -- ========================================================

    c.[Customer],
    c.[Category] AS [Customer Category],
    c.[Buying Group],

    -- ========================================================
    -- Product attributes
    -- ========================================================

    si.[Stock Item],
    si.[Brand],
    si.[Color],
    si.[Size],
    si.[Selling Package],
    si.[Is Chiller Stock],

    -- ========================================================
    -- Geographic attributes
    -- ========================================================

    city.[City],
    city.[State Province],
    city.[Country],

    -- ========================================================
    -- Transaction attributes
    -- ========================================================

    s.[Description],
    s.[Package],
    s.[Quantity],
    s.[Unit Price],
    s.[Tax Rate],

    s.[Total Excluding Tax],
    s.[Tax Amount],
    s.[Profit],
    s.[Total Including Tax],

    s.[Total Dry Items],
    s.[Total Chiller Items],

    -- ========================================================
    -- Derived business metrics
    -- ========================================================

    CAST(
        s.[Profit]
        / NULLIF(s.[Total Excluding Tax], 0)
        * 100.0
        AS decimal(10,2)
    ) AS [Profit Margin Percent],

    CASE
        WHEN s.[Delivery Date Key] IS NULL
            THEN NULL

        ELSE
            DATEDIFF(
                DAY,
                s.[Invoice Date Key],
                s.[Delivery Date Key]
            )
    END AS [Delivery Days],

    CASE
        WHEN s.[Delivery Date Key] IS NULL
            THEN 'Not Delivered'

        WHEN DATEDIFF(
            DAY,
            s.[Invoice Date Key],
            s.[Delivery Date Key]
        ) = 0
            THEN 'Same Day'

        WHEN DATEDIFF(
            DAY,
            s.[Invoice Date Key],
            s.[Delivery Date Key]
        ) = 1
            THEN 'Next Day'

        WHEN DATEDIFF(
            DAY,
            s.[Invoice Date Key],
            s.[Delivery Date Key]
        ) BETWEEN 2 AND 3
            THEN '2-3 Days'

        ELSE '4+ Days'
    END AS [Delivery Speed Category],

    CASE
        WHEN s.[Profit] < 0
            THEN 1
        ELSE 0
    END AS [Is Loss Making],

    CASE
        WHEN s.[Profit] < 0
            THEN 'Loss Making'

        WHEN s.[Profit] = 0
            THEN 'Break Even'

        ELSE 'Profitable'
    END AS [Profitability Status]

FROM Fact.[Sale] AS s

LEFT JOIN Dimension.[Customer] AS c
    ON s.[Customer Key] = c.[Customer Key]

LEFT JOIN Dimension.[Stock Item] AS si
    ON s.[Stock Item Key] = si.[Stock Item Key]

LEFT JOIN Dimension.[City] AS city
    ON s.[City Key] = city.[City Key];
GO
