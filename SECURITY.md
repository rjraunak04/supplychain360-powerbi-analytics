# Security Policy

## Supported project state

This repository is a portfolio/reference implementation. Security issues in model logic, RLS configuration, credential handling, SQL scripts or deployment documentation should be treated seriously.

## Reporting a security issue

Do not open a public issue containing:
- real tenant IDs
- passwords
- SQL credentials
- service-principal secrets
- gateway recovery keys
- production server names
- personal user-access mappings

For a private portfolio repository, report sensitive findings directly to the repository owner.

## Credential policy

This repository must never contain:
- `.env` secrets
- Power BI local cache files
- PBIX/PBIT binaries with embedded credentials
- gateway secrets
- production UPN mapping exports
- Azure/Fabric client secrets

Only demonstration identities such as `@contoso.com` are permitted in checked-in security examples.

## RLS note

The checked-in `Security User Access` table is a demo mapping. Replace it with a governed source before production use and test with real Viewer identities in Power BI Service.
