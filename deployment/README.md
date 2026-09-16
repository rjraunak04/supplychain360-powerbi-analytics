# Deployment Assets

This directory contains non-secret deployment templates for SupplyChain360.

## Environments

See `environments.example.json` for the expected semantic-model parameters.

Never store credentials in this file.

## Release lifecycle

### DEV
- author PBIP
- run SQL validation
- run static quality gate
- local Refresh All
- developer RLS test

### TEST
- deploy model/report
- map TEST parameters
- validate gateway
- reconcile KPIs
- run UAT
- test Viewer/RLS access
- record Performance Analyzer baseline

### PROD
- promote approved artifact
- map PROD parameters
- validate gateway credentials
- enable scheduled/incremental refresh
- validate RLS memberships
- smoke-test top report pages
- capture refresh evidence
- tag release

## Rollback

Keep each deployment tied to a Git commit/tag. If a deployment fails, redeploy the last known-good PBIP source rather than editing production ad hoc.
