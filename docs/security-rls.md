# Security & Row-Level Security

## Purpose

SupplyChain360 includes a production-style RLS pattern so the same semantic model can serve executives and regional managers without duplicating reports.

## Implemented roles

### Executive
- Model permission: read
- No row filters
- Intended for enterprise-wide leadership access

### Regional Manager
- Model permission: read
- Dynamic row filter on `Dim City`
- User identity resolved with `USERPRINCIPALNAME()`
- Access is controlled by the hidden `Security User Access` mapping table

The semantic model includes sample UPN-to-state mappings for demonstration only. Replace sample `@contoso.com` entries with a governed security mapping source before production deployment.

## Production pattern

Recommended production mapping columns:

| Column | Purpose |
|---|---|
| UserPrincipalName | Login/UPN returned by Power BI |
| State Province | Authorized state |
| AccessLevel | Optional governance label |
| EffectiveFrom / EffectiveTo | Optional temporal access control |
| IsActive | Optional access flag |

For large organizations, source the mapping table from a governed SQL table, Microsoft Entra-backed process, or approved master-data workflow instead of hard-coded demo rows.

## Validation

1. Open Power BI Desktop.
2. Use **Modeling → View as**.
3. Select `Regional Manager`.
4. Test with a UPN present in the mapping table.
5. Confirm only authorized states remain visible across Sales, Orders, Customers and City-filtered visuals.
6. Publish to Power BI Service.
7. Assign users/groups to semantic-model roles.
8. Test with actual viewer accounts.

## Security principles

- Apply RLS on dimension tables rather than facts where possible.
- Keep security mapping tables hidden from report authors.
- Use `USERPRINCIPALNAME()` consistently for dynamic identity.
- Do not grant workspace Contributor/Member/Admin access to users who must be restricted by RLS; validate workspace permissions separately.
- Never commit real user emails, tenant IDs, client secrets, gateway credentials or service-principal secrets to Git.

## Production acceptance criteria

- Regional users cannot see unauthorized states.
- Executive role sees enterprise-wide data.
- No report page bypasses dimension-based filtering.
- Service role membership is documented.
- RLS is tested with real viewer identities after publication.
