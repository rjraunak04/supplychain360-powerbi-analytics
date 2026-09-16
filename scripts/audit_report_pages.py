#!/usr/bin/env python3
"""Page-by-page PBIR audit for SupplyChain360.

Validates every registered report page against the checked-in TMDL semantic
model. This is a static/source QA gate; interactive Desktop rendering,
capacity/licensing and service refresh still require Power BI runtime.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "powerbi" / "SupplyChain360.Report" / "definition"
MODEL = ROOT / "powerbi" / "SupplyChain360.SemanticModel" / "definition"
TABLES = MODEL / "tables"
ERRORS: list[str] = []

EXPECTED_PAGES = [
    "01 Executive Overview",
    "02 Inventory Intelligence",
    "03 Inventory Risk Detail",
    "04 Procurement & Supplier Performance",
    "05 Supplier Exceptions & Procurement Risk",
    "06 Order Fulfillment & Backorders",
    "07 Fulfillment Exceptions",
    "08 Sales & Demand Intelligence",
    "09 Profitability & Customer Insights",
    "10 Stock Movement & Operations",
    "11 Movement Exceptions",
    "12 Product 360",
    "13 Supplier 360",
    "14 Data Quality & Model QA",
]

def fail(msg: str) -> None:
    ERRORS.append(msg)

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}

def parse_model():
    columns: dict[str, set[str]] = {}
    measures: dict[str, set[str]] = {}
    for path in TABLES.glob("*.tmdl"):
        text = path.read_text(encoding="utf-8")
        table_match = re.search(r"^table (?:'([^']+)'|([^\n]+))", text, re.M)
        table = (table_match.group(1) or table_match.group(2)).strip() if table_match else path.stem
        cols = set()
        ms = set()
        for m in re.finditer(r"^\tcolumn (?:'([^']+)'|([^\n]+))", text, re.M):
            cols.add((m.group(1) or m.group(2)).strip())
        for m in re.finditer(r"^\tmeasure (?:'([^']+)'|([^=\n]+?))\s*=", text, re.M):
            ms.add((m.group(1) or m.group(2)).strip())
        columns[table] = cols
        measures[table] = ms
    return columns, measures

def iter_field_refs(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ("Column", "Measure") and isinstance(value, dict):
                expr = value.get("Expression", {})
                entity = expr.get("SourceRef", {}).get("Entity")
                prop = value.get("Property")
                if entity and prop:
                    yield key, entity, prop
            yield from iter_field_refs(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_field_refs(item)

def main() -> int:
    columns, measures = parse_model()
    if not columns:
        fail("No TMDL tables parsed")

    pages_meta = load_json(REPORT / "pages" / "pages.json")
    page_ids = pages_meta.get("pageOrder") or []
    if len(page_ids) != 14:
        fail(f"Expected 14 registered pages; found {len(page_ids)}")

    rows = []
    page_names = []
    page_measure_refs: dict[str, set[str]] = {}

    for page_id in page_ids:
        page_dir = REPORT / "pages" / page_id
        page = load_json(page_dir / "page.json")
        name = page.get("displayName", page_id)
        page_names.append(name)

        visuals_dir = page_dir / "visuals"
        visual_files = sorted(visuals_dir.glob("*/visual.json")) if visuals_dir.exists() else []
        types = Counter()
        refs = set()
        data_visuals = 0

        if not visual_files:
            fail(f"{name}: no visuals found")

        for vf in visual_files:
            visual = load_json(vf)
            v = visual.get("visual")
            if isinstance(v, dict):
                vtype = v.get("visualType")
                if vtype:
                    types[vtype] += 1
                    if vtype not in ("textbox", "shape", "image"):
                        data_visuals += 1

                query = v.get("query", {})
                qstate = query.get("queryState", {}) if isinstance(query, dict) else {}
                if isinstance(qstate, dict) and "sortDefinition" in qstate:
                    fail(f"{name}: {vf.parent.name} has invalid queryState.sortDefinition")

            for kind, entity, prop in iter_field_refs(visual):
                refs.add((kind, entity, prop))
                if entity not in columns:
                    fail(f"{name}: visual references unknown table {entity}")
                    continue
                if kind == "Column" and prop not in columns.get(entity, set()):
                    fail(f"{name}: visual references missing column {entity}[{prop}]")
                if kind == "Measure" and prop not in measures.get(entity, set()):
                    fail(f"{name}: visual references missing measure {entity}[{prop}]")

        if data_visuals == 0:
            fail(f"{name}: page has no data visuals (blank report page)")

        measure_names = {prop for kind, entity, prop in refs if kind == "Measure"}
        page_measure_refs[name] = measure_names
        rows.append((name, len(visual_files), data_visuals, len(refs), dict(types)))

    if page_names != EXPECTED_PAGES:
        fail("Registered page names/order do not match the official 14-page catalog")

    # Regression gates for issues previously observed in Desktop screenshots.
    measures_text = (TABLES / "_Measures.tmdl").read_text(encoding="utf-8")
    if "'Fact Sales Demand'[Is Loss Making] = TRUE()" in measures_text:
        fail("Profitability measures compare int64 Is Loss Making to TRUE(); use = 1")
    for required in ("Loss Making Revenue", "Loss Making Line %", "Loss Making Lines"):
        if required not in measures.get("_Measures", set()):
            fail(f"Missing profitability measure: {required}")

    p7 = page_measure_refs.get("07 Fulfillment Exceptions", set())
    if "Top 10 City Backordered Units" in p7:
        fail("Page 07 still uses high-cardinality City backorder ranking")
    if "Top 10 State Backordered Units" not in p7:
        fail("Page 07 missing State backorder hotspot measure")

    p9 = page_measure_refs.get("09 Profitability & Customer Insights", set())
    for required in ("Loss Making Revenue", "Loss Making Line %", "Loss Making Lines"):
        if required not in p9:
            fail(f"Page 09 missing card measure: {required}")

    p14 = page_measure_refs.get("14 Data Quality & Model QA", set())
    for required in ("Inventory QA Status", "Inventory Key QA", "Latest Sales Date",
                     "Latest Order Date", "Latest Movement Date"):
        if required not in p14:
            fail(f"Page 14 QA missing measure: {required}")

    print("SupplyChain360 page-by-page report audit")
    print("=" * 92)
    for name, visuals, data_visuals, refs, types in rows:
        chart_count = sum(v for k, v in types.items()
                          if k not in ("textbox", "slicer", "cardVisual", "tableEx"))
        print(f"[PASS] {name:<43} visuals={visuals:>2} data={data_visuals:>2} refs={refs:>2} charts={chart_count:>2}")
    print("=" * 92)

    if ERRORS:
        print("PAGE AUDIT: FAIL")
        for err in ERRORS:
            print(f" - {err}")
        return 1

    print("PAGE AUDIT: PASS — all 14 registered pages are structurally valid against the semantic model.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
