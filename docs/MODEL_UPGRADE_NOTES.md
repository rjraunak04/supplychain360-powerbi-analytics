# SupplyChain360 Semantic Model Upgrade

This PBIP was cleaned and upgraded to a production-style star-schema foundation.

## Changes applied
- Removed duplicated descriptive attributes from fact tables at the Power Query source-selection layer.
- Disabled Power BI auto date/time local tables and removed generated LocalDateTable objects.
- Marked `Dim Date` as the time dimension and configured month sorting.
- Rebuilt relationships as single-direction dimension-to-fact relationships.
- Added inactive role-playing relationships for Picked Date, Delivery Date, and Bill-To Customer.
- Removed fact-to-fact and description-based auto-detected relationships.
- Hid technical surrogate keys, source IDs, SCD validity columns, and lineage keys.
- Added geographic data categories for City, State/Province, Country, Continent, and Postal Code.
- Added a centralized `_Measures` table with inventory, procurement, fulfillment, sales, time-intelligence, and stock-movement measures.
- Renamed the initial report page to `01 Executive Overview`.
- Removed local cache files from the portable package.

## Important after opening
1. Open `SupplyChain360.pbip` in Power BI Desktop.
2. Refresh against `localhost / WideWorldImportersDW`.
3. Confirm there are no relationship, refresh, or DAX errors.
4. Validate KPI values against the SQL benchmark scripts before building visuals.

## Current source-model limitation
`Fact Order Fulfillment` does not currently expose City/Salesperson/Picker keys from the SQL analytics view. Those relationships were intentionally not fabricated. Add those keys to the SQL view later if city-level fulfillment or picker/salesperson analysis is required.
