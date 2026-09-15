USE WideWorldImportersDW;
GO

-- Overall Sales KPIs
SELECT
    COUNT(*) AS SalesLines,
    COUNT(DISTINCT [WWI Invoice ID]) AS TotalInvoices,
    SUM([Quantity]) AS TotalQuantitySold,
    SUM([Total Excluding Tax]) AS Revenue,
    SUM([Profit]) AS Profit
FROM analytics.vw_sales_demand;
GO


-- Profitability Status
SELECT
    [Profitability Status],
    COUNT(*) AS SalesLines,
    SUM([Total Excluding Tax]) AS Revenue,
    SUM([Profit]) AS Profit
FROM analytics.vw_sales_demand
GROUP BY [Profitability Status];
GO


-- Delivery Performance
SELECT
    [Delivery Speed Category],
    COUNT(DISTINCT [WWI Invoice ID]) AS Invoices,
    AVG(CAST([Delivery Days] AS decimal(10,2))) AS AvgDeliveryDays
FROM analytics.vw_sales_demand
GROUP BY [Delivery Speed Category];
GO
