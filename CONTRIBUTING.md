# Contributing

## Change flow

1. Create a focused branch.
2. Make one logical change.
3. Run:
   ```bash
   python scripts/validate_powerbi_project.py
   ```
4. Refresh the PBIP in Power BI Desktop when model/report behavior changes.
5. Reconcile affected KPIs against SQL validation queries.
6. Update documentation.
7. Open a pull request.
8. Merge only after the GitHub Actions quality gate passes.

## Commit convention

Use Conventional Commit-style prefixes:

- `feat:` new capability
- `fix:` bug fix
- `docs:` documentation
- `test:` validation/tests
- `perf:` performance improvement
- `refactor:` non-functional restructure
- `chore:` maintenance

## Power BI source-control rules

- Commit PBIP/PBIR/TMDL source.
- Do not commit PBIX/PBIT binaries.
- Do not commit `.pbi` local cache.
- Keep technical keys hidden unless required.
- Prefer explicit measures to implicit aggregations.
- Do not add fact-to-fact relationships without an architecture decision.
- Document new measures in `docs/dax-measures.md`.

## SQL rules

- Keep reusable analytics logic in `sql/views/`.
- Add or update reconciliation tests in `sql/validation/`.
- State the expected grain in comments.
- Avoid environment-specific credentials or server names.

## Definition of Done

A change is done when:
- static CI passes
- local runtime refresh passes when applicable
- affected KPIs reconcile
- security behavior is preserved
- README/docs remain accurate
