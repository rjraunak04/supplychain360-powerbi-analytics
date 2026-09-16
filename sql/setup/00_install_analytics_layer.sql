-- ============================================================
-- SupplyChain360 — Analytics Layer Installer
-- Run this entire script in SSMS against the local SQL Server.
-- Safe to re-run because the view scripts use CREATE OR ALTER VIEW.
-- ============================================================

-- ============================================================
-- SOURCE: sql/views/01_vw_inventory.sql
-- ============================================================
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
        AS [Stock Above Reorder],

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

INNER JOIN Dimension.[Stock Item] AS si
    ON sh.[Stock Item Key] = si.[Stock Item Key]
   AND CAST(si.[Valid To] AS date) = '9999-12-31';
GO

-- ============================================================
-- SOURCE: sql/views/02_vw_procurement.sql
-- ============================================================
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

-- ============================================================
-- SOURCE: sql/views/03_vw_order_fulfillment.sql
-- ============================================================
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

-- ============================================================
-- SOURCE: sql/views/04_vw_sales_demand.sql
-- ============================================================
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

-- ============================================================
-- SOURCE: sql/views/05_vw_stock_movement.sql
-- ============================================================
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


-- ============================================================
-- POST-INSTALL VERIFICATION
-- ============================================================
USE WideWorldImportersDW;
GO

SELECT
    s.name AS [Schema],
    v.name AS [View],
    CASE
        WHEN v.name IN (
            'vw_inventory',
            'vw_procurement',
            'vw_order_fulfillment',
            'vw_sales_demand',
            'vw_stock_movement'
        ) THEN 'EXPECTED'
        ELSE 'OTHER'
    END AS [Status]
FROM sys.views v
JOIN sys.schemas s
    ON v.schema_id = s.schema_id
WHERE s.name = 'analytics'
ORDER BY v.name;
GO

SELECT
    (SELECT COUNT_BIG(*) FROM analytics.vw_inventory) AS InventoryRows,
    (SELECT COUNT_BIG(*) FROM analytics.vw_procurement) AS ProcurementRows,
    (SELECT COUNT_BIG(*) FROM analytics.vw_order_fulfillment) AS FulfillmentRows,
    (SELECT COUNT_BIG(*) FROM analytics.vw_sales_demand) AS SalesRows,
    (SELECT COUNT_BIG(*) FROM analytics.vw_stock_movement) AS MovementRows;
GO
