# SupplyChain360 — DAX Measures

This document contains the core business measures used in the Power BI semantic model.  
All production measures are maintained in the centralized `_Measures` table inside the PBIP semantic model.

---

## 1. Inventory Measures

### Total Inventory Value
```DAX
Total Inventory Value =
SUM('Fact Inventory'[Inventory Value])
```

### Quantity On Hand
```DAX
Quantity On Hand =
SUM('Fact Inventory'[Quantity On Hand])
```

### Stockout SKUs
```DAX
Stockout SKUs =
CALCULATE(
    DISTINCTCOUNT('Fact Inventory'[Stock Item Key]),
    'Fact Inventory'[Inventory Status] = "Stockout"
)
```

### Reorder Required SKUs
```DAX
Reorder Required SKUs =
CALCULATE(
    DISTINCTCOUNT('Fact Inventory'[Stock Item Key]),
    'Fact Inventory'[Inventory Status] = "Reorder Required"
)
```

### Overstock SKUs
```DAX
Overstock SKUs =
CALCULATE(
    DISTINCTCOUNT('Fact Inventory'[Stock Item Key]),
    'Fact Inventory'[Inventory Status] = "Overstock"
)
```

### Healthy SKUs
```DAX
Healthy SKUs =
CALCULATE(
    DISTINCTCOUNT('Fact Inventory'[Stock Item Key]),
    'Fact Inventory'[Inventory Status] = "Healthy"
)
```

### Inventory Health %
```DAX
Inventory Health % =
DIVIDE(
    [Healthy SKUs],
    DISTINCTCOUNT('Fact Inventory'[Stock Item Key])
)
```

---

## 2. Procurement Measures

### Purchase Orders
```DAX
Purchase Orders =
DISTINCTCOUNT('Fact Procurement'[WWI Purchase Order ID])
```

### Ordered Quantity
```DAX
Ordered Quantity =
SUM('Fact Procurement'[Ordered Quantity])
```

### Received Quantity
```DAX
Received Quantity =
SUM('Fact Procurement'[Received Quantity])
```

### Outstanding Quantity
```DAX
Outstanding Quantity =
SUM('Fact Procurement'[Outstanding Quantity])
```

### Procurement Fulfillment %
```DAX
Procurement Fulfillment % =
DIVIDE(
    [Received Quantity],
    [Ordered Quantity]
)
```

---

## 3. Order Fulfillment Measures

### Total Orders
```DAX
Total Orders =
DISTINCTCOUNT('Fact Order Fulfillment'[WWI Order ID])
```

### Order Lines
```DAX
Order Lines =
COUNTROWS('Fact Order Fulfillment')
```

### Ordered Units
```DAX
Ordered Units =
SUM('Fact Order Fulfillment'[Quantity])
```

### Backordered Lines
```DAX
Backordered Lines =
SUM('Fact Order Fulfillment'[Is Backordered])
```

### Backorder Rate %
```DAX
Backorder Rate % =
DIVIDE(
    [Backordered Lines],
    [Order Lines]
)
```

### Order Value
```DAX
Order Value =
SUM('Fact Order Fulfillment'[Total Including Tax])
```

### Pending Pick Lines
```DAX
Pending Pick Lines =
CALCULATE(
    COUNTROWS('Fact Order Fulfillment'),
    'Fact Order Fulfillment'[Fulfillment Status] = "Pending Pick"
)
```

### Average Days to Pick
```DAX
Average Days to Pick =
AVERAGE('Fact Order Fulfillment'[Days To Pick])
```

---

## 4. Sales & Demand Measures

### Total Revenue
```DAX
Total Revenue =
SUM('Fact Sales Demand'[Total Excluding Tax])
```

### Total Profit
```DAX
Total Profit =
SUM('Fact Sales Demand'[Profit])
```

### Profit Margin %
```DAX
Profit Margin % =
DIVIDE(
    [Total Profit],
    [Total Revenue]
)
```

### Units Sold
```DAX
Units Sold =
SUM('Fact Sales Demand'[Quantity])
```

### Total Invoices
```DAX
Total Invoices =
DISTINCTCOUNT('Fact Sales Demand'[WWI Invoice ID])
```

### Average Delivery Days
```DAX
Average Delivery Days =
AVERAGE('Fact Sales Demand'[Delivery Days])
```

---

## 5. Time Intelligence

### Revenue YTD
```DAX
Revenue YTD =
TOTALYTD(
    [Total Revenue],
    'Dim Date'[Date]
)
```

### Revenue Last Year
```DAX
Revenue LY =
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR('Dim Date'[Date])
)
```

### Revenue YoY %
```DAX
Revenue YoY % =
DIVIDE(
    [Total Revenue] - [Revenue LY],
    [Revenue LY]
)
```

### Profit YTD
```DAX
Profit YTD =
TOTALYTD(
    [Total Profit],
    'Dim Date'[Date]
)
```

---

## 6. Role-Playing Relationship Measures

### Revenue by Delivery Date
Uses the inactive Delivery Date relationship.

```DAX
Revenue by Delivery Date =
CALCULATE(
    [Total Revenue],
    USERELATIONSHIP(
        'Dim Date'[Date],
        'Fact Sales Demand'[Delivery Date Key]
    )
)
```

### Revenue by Bill-To Customer
Uses the inactive Bill-To Customer relationship.

```DAX
Revenue by Bill-To Customer =
CALCULATE(
    [Total Revenue],
    USERELATIONSHIP(
        'Dim Customer'[Customer Key],
        'Fact Sales Demand'[Bill To Customer Key]
    )
)
```

### Orders by Picked Date
Uses the inactive Picked Date relationship.

```DAX
Orders by Picked Date =
CALCULATE(
    [Total Orders],
    USERELATIONSHIP(
        'Dim Date'[Date],
        'Fact Order Fulfillment'[Picked Date Key]
    )
)
```

---

## 7. Stock Movement Measures

### Stock In Quantity
```DAX
Stock In Quantity =
SUM('Fact Stock Movement'[Stock In Quantity])
```

### Stock Out Quantity
```DAX
Stock Out Quantity =
SUM('Fact Stock Movement'[Stock Out Quantity])
```

### Net Stock Movement
```DAX
Net Stock Movement =
SUM('Fact Stock Movement'[Quantity])
```

### Movement Events
```DAX
Movement Events =
COUNTROWS('Fact Stock Movement')
```

---

## Measure Design Principles

- Measures are centralized in the `_Measures` table.
- Row-level business logic is calculated in SQL views where practical.
- Dynamic aggregation and time intelligence are implemented in DAX.
- `DIVIDE()` is preferred over direct division to safely handle zero denominators.
- `USERELATIONSHIP()` is used for inactive role-playing relationships.
- Measures are designed to respond to dimension filters and slicers.
- Power BI KPI values should reconcile with the SQL benchmark queries in `sql/validation/07_executive_kpi_benchmark.sql`.
