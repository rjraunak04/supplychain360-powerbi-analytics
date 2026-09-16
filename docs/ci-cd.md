# CI/CD Strategy

## Continuous Integration

Workflow: `.github/workflows/powerbi-ci.yml`

Triggered on:
- push to `main`
- pull request targeting `main`

Checks:
- PBIP/PBIR/TMDL structure
- report JSON validity
- page registration
- relationship references
- environment parameters
- RLS metadata
- incremental refresh range filters
- SQL assets
- accidental PBIX/PBIT binaries
- DAX measure-layer coverage

The workflow uses only the repository and Python standard library, so it does not require Power BI credentials.

## Release Packaging

Workflow: `.github/workflows/package-release.yml`

Triggered by:
- manual workflow dispatch
- tags matching `v*`

Flow:
1. Checkout source.
2. Run static quality gate.
3. Build a clean source ZIP.
4. Upload the ZIP as a GitHub Actions artifact.

The release packager excludes:
- PBIX/PBIT binaries
- `.pbi` caches
- Git metadata
- environment files/secrets
- local temporary artifacts

## Power BI Service deployment

Automatic Service deployment is intentionally not performed from this public portfolio pipeline because it would require tenant-specific authentication, workspace IDs and deployment credentials.

A production organization can extend this pattern with:
- Fabric/Power BI deployment pipelines
- service-principal authentication
- approved secret storage
- parameter rules for DEV/TEST/PROD
- post-deployment refresh/RLS smoke tests

## Release versioning

Recommended semantic version tags:

- `v1.0.0` — first fully runtime-validated portfolio release
- patch — documentation/bug fix
- minor — new analytical capability
- major — breaking semantic-model redesign

Do not tag `v1.0.0` until local Refresh All, RLS validation and final screenshots are complete.
