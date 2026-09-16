# Performance Engineering

## Goal

A portfolio dashboard should not only look correct; it should also demonstrate performance discipline.

## Static optimizations already present

- Star-schema modeling
- Conformed dimensions
- Hidden technical keys
- Centralized explicit measures
- Display folders for measures
- Source-side SQL analytics views
- Selected-column projection in Power Query
- Environment parameterization
- Date-range filters on large transactional facts
- No PBIX binary in source control

## Runtime performance budget

Use Power BI Performance Analyzer after a successful refresh.

Recommended targets for this portfolio:

| Metric | Target |
|---|---:|
| Executive page initial visual completion | < 5 s on local machine |
| Typical individual visual | < 1.5 s |
| Complex ranking/table visual | < 3 s |
| User interaction/filter response | < 2 s |
| Refresh | Record baseline and optimize regressions |

These are project targets, not universal Power BI SLAs.

## Performance Analyzer procedure

1. Open **Optimize → Performance Analyzer**.
2. Start recording.
3. Refresh visuals.
4. Export/capture results for pages 01, 02, 04, 06, 08 and 12.
5. Record the slowest visuals.
6. Check whether time is dominated by DAX query, visual display or other processing.
7. Optimize and repeat.

## DAX review checklist

- Prefer measures over calculated columns for dynamic aggregations.
- Use `DIVIDE()` for safe ratios.
- Avoid unnecessary iterators over large fact tables.
- Keep ranking measures scoped with `ALLSELECTED()` only where interactive ranking is required.
- Avoid bi-directional relationships unless justified.
- Verify role-playing date measures use `USERELATIONSHIP()`.
- Remove unused columns from fact queries.

## Model-size checklist

- Hide surrogate keys.
- Avoid high-cardinality text columns in facts unless required.
- Move descriptive attributes to dimensions.
- Use integer keys for relationships.
- Keep raw identifiers hidden from report consumers.

## Evidence to capture before portfolio publication

Create screenshots or CSV exports showing:

- Performance Analyzer results
- Model view
- Refresh success
- Data Quality & Model QA page
- Final Executive Overview

Store screenshots under `docs/images/` and reference them from the README.
