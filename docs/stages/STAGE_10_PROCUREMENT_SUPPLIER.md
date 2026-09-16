# Stage 10 — Procurement & Supplier Performance Intelligence

## Pages added
- 04 Procurement & Supplier Performance
- 05 Supplier Exceptions & Procurement Risk

## Business questions answered
- How much procurement volume is flowing through each supplier?
- What share of ordered quantity has been received?
- Which suppliers carry the largest outstanding quantity exposure?
- Which products drive current procurement shortfalls?
- How many purchase orders are open versus finalized?
- What is the weighted expected lead-time profile of current procurement?

## Important interpretation
`Average Expected Lead Time Days` is based on the product master expected lead time from `Dim Stock Item`. It is not an observed supplier delivery lead-time KPI.

## Runtime validation
Open `SupplyChain360.pbip`, refresh against `localhost / WideWorldImportersDW`, and validate that both new pages render without model errors.
