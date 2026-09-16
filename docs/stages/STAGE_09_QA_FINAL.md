# Stage 09 QA — Final

## QA fixes applied
- Inventory is constrained to **current Stock Item SCD rows** (`Valid To = 9999-12-31`).
- Historical Stock Item surrogate versions no longer inflate current-state inventory analysis.
- Added a unique business-friendly **SKU Label** for risk detail and slicers.
- Inventory Status now has a deterministic severity sort order.
- SKU Risk Register now uses measures rather than raw additive fact columns, so it renders one analytical SKU row per context.
- Added inventory model QA measures (`Inventory Rows`, `Inventory Key QA`, `Inventory QA Status`).
- Added `Excess Inventory % of Value` and `Reorder Exposure % of Value`.
- Inventory pages explicitly state that they represent the **current-state snapshot**.

## Runtime acceptance checks
After refresh in Power BI Desktop:
1. `Inventory QA Status` should return **PASS**.
2. `Inventory Key QA` should return **0**.
3. Risk register should no longer show historical duplicate SKU versions.
4. Inventory totals should reflect current Stock Item versions only.
5. Inventory Status order should be Stockout → Reorder Required → Overstock → Healthy.
