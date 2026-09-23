"""Parameterized, read-only queries over governed analytics views."""

DOMAIN_QUERIES = {
    "inventory": """
        SELECT TOP (?) [Stock Item], [Brand], [Quantity On Hand], [Reorder Level],
               [Target Stock Level], [Inventory Value], [Inventory Status],
               [Suggested Reorder Quantity]
        FROM analytics.vw_inventory
        WHERE [Needs Reorder] = 1 OR [Is Stockout] = 1
        ORDER BY [Is Stockout] DESC, [Suggested Reorder Quantity] DESC
    """,
    "procurement": """
        SELECT TOP (?) [Supplier], [Stock Item], [WWI Purchase Order ID],
               [Ordered Quantity], [Received Quantity], [Outstanding Quantity],
               [Receipt Fulfillment Percent], [Receipt Status], [Purchase Order Status]
        FROM analytics.vw_procurement
        WHERE [Outstanding Quantity] > 0 OR [Purchase Order Status] = 'Open'
        ORDER BY [Outstanding Quantity] DESC
    """,
    "fulfillment": """
        SELECT TOP (?) [Customer], [Stock Item], [WWI Order ID], [Quantity],
               [Backordered Quantity], [Days To Pick], [Fulfillment Status],
               [Picking Speed Category]
        FROM analytics.vw_order_fulfillment
        WHERE [Is Backordered] = 1 OR [Is Picked] = 0
        ORDER BY [Backordered Quantity] DESC, [Quantity] DESC
    """,
    "sales": """
        SELECT TOP (?) [Stock Item], SUM([Quantity]) AS [Units Sold],
               SUM([Total Excluding Tax]) AS [Revenue], SUM([Profit]) AS [Profit]
        FROM analytics.vw_sales_demand
        GROUP BY [Stock Item]
        ORDER BY [Revenue] DESC
    """,
}
