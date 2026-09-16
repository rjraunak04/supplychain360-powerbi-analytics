# Object-Level Security (OLS) — Optional Production Extension

SupplyChain360 implements dynamic RLS because row filtering is directly relevant to regional management.

OLS is documented as an optional extension rather than being enabled in the portfolio model by default.

## Why OLS is not enabled by default

Hiding columns such as cost or profit from a role can cause visuals/measures that depend on those fields to become unavailable for that role. Enabling OLS without a separate role-specific report experience could reduce usability.

## Example production use case

A company may want regional operational users to see:
- inventory quantity
- fulfillment
- sales units

but not:
- Last Cost Price
- raw Profit
- sensitive employee/customer columns

In that scenario, create a separate restricted role and use TMDL table/column permissions with `metadataPermission: none`.

## Recommended implementation process

1. Identify sensitive columns.
2. Identify measures depending on those columns.
3. Design a restricted report experience.
4. Apply OLS to the restricted role.
5. Test every page with the restricted identity.
6. Validate export/analyze permissions.
7. Document the access matrix.

## Decision

RLS is active in the model.
OLS remains an explicitly documented optional control until a role-specific consumer experience is designed and runtime-tested.
