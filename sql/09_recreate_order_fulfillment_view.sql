USE WideWorldImportersDW;
GO

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'analytics')
    EXEC('CREATE SCHEMA analytics');
GO

CREATE OR ALTER VIEW analytics.vw_order_fulfillment
AS
SELECT
    o.[Order Key],
    o.[City Key],
    o.[Customer Key],
    o.[Stock Item Key],
    o.[Salesperson Key],
    o.[Picker Key],
    o.[Order Date Key],
    o.[Picked Date Key],
    o.[WWI Order ID],
    o.[WWI Backorder ID],
    o.[Quantity],
    o.[Unit Price],
    o.[Tax Rate],
    o.[Total Excluding Tax],
    o.[Tax Amount],
    o.[Total Including Tax],
    CASE WHEN o.[WWI Backorder ID] IS NULL THEN 0 ELSE 1 END AS [Is Backordered],
    CASE WHEN o.[WWI Backorder ID] IS NULL THEN 0 ELSE o.[Quantity] END AS [Backordered Quantity],
    CASE WHEN o.[Picked Date Key] IS NULL THEN 0 ELSE 1 END AS [Is Picked],
    CASE WHEN o.[Picked Date Key] IS NULL THEN NULL
         ELSE DATEDIFF(DAY, o.[Order Date Key], o.[Picked Date Key]) END AS [Days To Pick],
    CASE WHEN o.[WWI Backorder ID] IS NOT NULL THEN 'Backordered'
         WHEN o.[Picked Date Key] IS NULL THEN 'Pending Pick'
         ELSE 'Picked' END AS [Fulfillment Status],
    CASE WHEN o.[Picked Date Key] IS NULL THEN 'Not Completed'
         WHEN DATEDIFF(DAY, o.[Order Date Key], o.[Picked Date Key]) = 0 THEN 'Same Day'
         WHEN DATEDIFF(DAY, o.[Order Date Key], o.[Picked Date Key]) = 1 THEN 'Next Day'
         ELSE '2+ Days' END AS [Picking Speed Category]
FROM Fact.[Order] o;
GO
