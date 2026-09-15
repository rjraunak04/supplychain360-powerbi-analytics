# SupplyChain360 Semantic Model

## Fact Tables
- Fact Inventory
- Fact Procurement
- Fact Order Fulfillment
- Fact Sales Demand
- Fact Stock Movement

## Dimensions
- Dim Date
- Dim Stock Item
- Dim Supplier
- Dim Customer
- Dim City
- Dim Employee
- Dim Transaction Type

## Modeling Approach
- Star-schema design
- One-to-many dimension-to-fact relationships
- Single-direction filtering
- No fact-to-fact relationships
- Shared conformed dimensions
- Role-playing inactive relationships where required

## Inactive Relationships
- Dim Date → Picked Date
- Dim Date → Delivery Date
- Dim Customer → Bill To Customer
- Dim Employee → Picker
