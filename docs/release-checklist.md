# Release Gate Checklist

## Source control

- [ ] Working tree clean
- [ ] GitHub Actions quality gate passes
- [ ] No PBIX/PBIT binaries committed
- [ ] No secrets or real user mappings committed
- [ ] Changelog updated

## Database

- [ ] SQL analytics views created/updated
- [ ] SQL validation scripts pass
- [ ] Expected fact grains validated
- [ ] Headline KPI benchmarks reconcile

## Semantic model

- [ ] Refresh All succeeds
- [ ] Relationships valid
- [ ] Technical keys hidden
- [ ] Measures use expected formatting/display folders
- [ ] Role-playing relationships tested
- [ ] Parameter values correct for target environment
- [ ] RangeStart/RangeEnd logic folds where expected

## Security

- [ ] Executive role tested
- [ ] Regional Manager role tested
- [ ] Unmapped regional user receives no unauthorized data
- [ ] Power BI Service role membership reviewed
- [ ] Workspace permissions do not bypass intended restrictions

## Report

- [ ] All 14 pages render
- [ ] Core slicers interact correctly
- [ ] No broken visuals
- [ ] QA page passes
- [ ] Top exception tables show expected results
- [ ] Tooltips/drill paths reviewed
- [ ] Accessibility checklist complete
- [ ] Mobile layout reviewed

## Performance

- [ ] Performance Analyzer baseline captured
- [ ] Slowest visuals reviewed
- [ ] No unnecessary fact columns loaded
- [ ] No accidental bidirectional relationship added
- [ ] Page interaction performance acceptable

## Service

- [ ] Gateway mapping works
- [ ] On-demand refresh succeeds
- [ ] Scheduled refresh configured
- [ ] Refresh history captured
- [ ] RLS tested with Viewer identity
- [ ] Deployment notes completed

## Portfolio

- [ ] Executive screenshot
- [ ] Model screenshot
- [ ] Performance screenshot
- [ ] RLS evidence
- [ ] Refresh-history evidence
- [ ] README gallery updated
