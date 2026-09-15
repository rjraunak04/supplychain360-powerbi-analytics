# SupplyChain360 — Data Model

## Modeling Approach

SupplyChain360 uses a dimensional star-schema design.

The semantic model separates descriptive dimensions from
transactional fact tables to improve performance, usability
and DAX simplicity.

## Core Fact Tables

### Fact.Order
Represents customer order activity and demand.

Primary analytics:
- order volume
- ordered quantity
- picked quantity
- backorders
- fulfillment

### Fact.Purchase
Represents supplier procurement activity.

Primary analytics:
- purchase volume
- supplier activity
- quantities ordered and received
- procurement trends

### Fact.Stock Holding
Represents current inventory position.

Primary analytics:
- inventory on hand
- reorder levels
- target inventory
- inventory value

### Fact.Movement
Represents inventory movement events.

Primary analytics:
- stock inflow/outflow
- inventory activity
- transaction movement

### Fact.Sale
Represents completed sales transactions.

Primary analytics:
- revenue
- quantity sold
- profit
- product/customer demand

## Core Dimensions

- Dimension.Date
- Dimension.Stock Item
- Dimension.Supplier
- Dimension.Customer
- Dimension.City
- Dimension.Employee

## Modeling Rules

- Dimension-to-fact relationships use one-to-many cardinality.
- Dimensions filter fact tables.
- Single-direction filtering is preferred.
- Fact-to-fact relationships are avoided.
- Shared dimensions are reused across fact tables.
- Role-playing dates are implemented using active and inactive relationships.
