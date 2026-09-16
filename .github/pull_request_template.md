## Summary

Describe the business/model/report change.

## Change type

- [ ] SQL / source logic
- [ ] Power Query
- [ ] Semantic model / relationships
- [ ] DAX
- [ ] Report visuals / UX
- [ ] Security / RLS
- [ ] Performance
- [ ] Documentation / deployment

## Quality checklist

- [ ] `python scripts/validate_powerbi_project.py` passes
- [ ] Power BI Refresh All passes (if runtime behavior changed)
- [ ] Affected KPIs reconcile with SQL validation
- [ ] No PBIX/PBIT binary added
- [ ] No credentials / tenant IDs / real user mappings added
- [ ] RLS behavior validated when security logic changed
- [ ] Documentation updated
- [ ] Screenshots attached for visible report changes

## Evidence

Add screenshots, QA output or reconciliation notes.
