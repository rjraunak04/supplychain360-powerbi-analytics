# Final Architecture

## Fact domains
- Fact Inventory
- Fact Procurement
- Fact Order Fulfillment
- Fact Sales Demand
- Fact Stock Movement

## Conformed dimensions
- Dim Date
- Dim Stock Item
- Dim Supplier
- Dim Customer
- Dim City
- Dim Employee
- Dim Transaction Type

## Modeling principles
- One-to-many dimension-to-fact relationships
- Single-direction filtering
- No fact-to-fact relationships
- Inactive role-playing relationships for alternate dates and roles
- Centralized `_Measures` table
- Current-state inventory SCD protection
- PBIP/PBIR/TMDL source-control-friendly structure
