USE WideWorldImportersDW;
GO

-- Overall procurement KPIs
SELECT
    COUNT(*) AS PurchaseLines,
    COUNT(DISTINCT [WWI Purchase Order ID]) AS PurchaseOrders,
    SUM([Ordered Quantity]) AS TotalOrderedQuantity,
    SUM([Received Quantity]) AS TotalReceivedQuantity,
    SUM([Outstanding Quantity]) AS TotalOutstandingQuantity,
    CAST(
        100.0 * SUM([Received Quantity])
        / NULLIF(SUM([Ordered Quantity]), 0)
        AS decimal(10,2)
    ) AS OverallReceiptFulfillmentPercent
FROM analytics.vw_procurement;
GO

-- Supplier level validation
SELECT
    [Supplier],
    COUNT(DISTINCT [WWI Purchase Order ID]) AS PurchaseOrders,
    SUM([Ordered Quantity]) AS OrderedQuantity,
    SUM([Received Quantity]) AS ReceivedQuantity,
    SUM([Outstanding Quantity]) AS OutstandingQuantity,
    CAST(
        100.0 * SUM([Received Quantity])
        / NULLIF(SUM([Ordered Quantity]), 0)
        AS decimal(10,2)
    ) AS FulfillmentPercent
FROM analytics.vw_procurement
GROUP BY [Supplier]
ORDER BY FulfillmentPercent ASC;
GO
