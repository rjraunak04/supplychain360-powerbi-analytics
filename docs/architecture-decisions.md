# Architecture Decisions

## ADR-001 — Star schema over a flat reporting table

**Decision:** Use conformed dimensions with separate facts for Inventory, Procurement, Order Fulfillment, Sales Demand and Stock Movement.

**Why:** Preserves business grain, reduces duplicated attributes, supports reusable dimensions and enables cross-domain 360 analysis.

## ADR-002 — No direct fact-to-fact relationships

**Decision:** Facts interact through conformed dimensions.

**Why:** Avoids ambiguous filtering and preserves predictable measure behavior.

## ADR-003 — SQL for reusable row logic, DAX for analytical aggregation

**Decision:** Stable row-level business rules are primarily shaped in SQL analytics views/Power Query; interactive aggregation and context-aware KPIs are DAX measures.

**Why:** Keeps the semantic layer understandable and avoids duplicating complex row logic inside many measures.

## ADR-004 — PBIP/PBIR/TMDL source control

**Decision:** Store source-controlled project definitions instead of a large PBIX binary.

**Why:** Enables code review, Git diff, CI validation and reproducible semantic/report development.

## ADR-005 — Parameterized data source

**Decision:** Use ServerName and DatabaseName model parameters.

**Why:** Supports DEV/TEST/PROD promotion without editing every M query.

## ADR-006 — Dynamic RLS

**Decision:** Use USERPRINCIPALNAME() with an access-mapping table for the Regional Manager role.

**Why:** One role can securely serve many users with different regional scopes.

## ADR-007 — Incremental-refresh readiness

**Decision:** Apply RangeStart/RangeEnd filters to growing transactional facts.

**Why:** Provides a scalable deployment path while keeping the sample model fully testable locally.

## ADR-008 — Automated quality gate

**Decision:** Validate PBIR JSON, TMDL references, parameters, security metadata, SQL assets and repository hygiene in GitHub Actions.

**Why:** Treats BI artifacts as production code rather than manually managed desktop files.
