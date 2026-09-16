#!/usr/bin/env python3
"""Desktop-strict static quality gate for SupplyChain360.

Uses only Python standard library. The validator is intentionally stricter than
basic JSON parsing and checks PBIP/PBIR/TMDL structural requirements that Power
BI Desktop expects before materializing report exploration/pages.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POWERBI = ROOT / "powerbi"
PBIP = POWERBI / "SupplyChain360.pbip"
REPORT = POWERBI / "SupplyChain360.Report"
MODEL = POWERBI / "SupplyChain360.SemanticModel"
REPORT_DEF = REPORT / "definition"
MODEL_DEF = MODEL / "definition"
TABLES = MODEL_DEF / "tables"
ERRORS: list[str] = []
WARNINGS: list[str] = []

PBIP_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json"
PBIR_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json"
PBISM_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json"
VERSION_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json"
PAGES_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"
PAGE_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
VISUAL_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json"
REPORT_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json"
HEX20 = re.compile(r"^[0-9a-f]{20}$")


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        ERRORS.append(f"Cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def load_json(path: Path) -> dict:
    try:
        return json.loads(read(path))
    except Exception as exc:
        ERRORS.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}


def validate_json_tree(path: Path) -> int:
    count = 0
    for file in path.rglob("*.json"):
        count += 1
        try:
            json.loads(file.read_text(encoding="utf-8"))
        except Exception as exc:
            ERRORS.append(f"Invalid JSON {file.relative_to(ROOT)}: {exc}")
    return count


def main() -> int:
    required = [
        PBIP,
        REPORT / ".platform",
        REPORT / "definition.pbir",
        REPORT_DEF / "version.json",
        REPORT_DEF / "report.json",
        REPORT_DEF / "pages" / "pages.json",
        MODEL / ".platform",
        MODEL / "definition.pbism",
        MODEL_DEF / "model.tmdl",
        MODEL_DEF / "relationships.tmdl",
        TABLES / "_Measures.tmdl",
        TABLES / "Security User Access.tmdl",
        ROOT / "README.md",
        ROOT / ".gitignore",
    ]
    for path in required:
        check(path.exists(), f"Missing required asset: {path.relative_to(ROOT)}")

    # Desktop-strict PBIP/PBIR scaffold checks.
    pbip = load_json(PBIP)
    check(pbip.get("$schema") == PBIP_SCHEMA, "SupplyChain360.pbip missing/incorrect required $schema")
    check(pbip.get("version") == "1.0", "SupplyChain360.pbip version must be 1.0")
    artifacts = pbip.get("artifacts") or []
    check(
        len(artifacts) == 1 and artifacts[0].get("report", {}).get("path") == "SupplyChain360.Report",
        "PBIP report pointer must target SupplyChain360.Report",
    )

    pbir = load_json(REPORT / "definition.pbir")
    check(pbir.get("$schema") == PBIR_SCHEMA, "definition.pbir missing/incorrect required $schema")
    check(pbir.get("version") == "4.0", "definition.pbir version must be 4.0")
    check(
        pbir.get("datasetReference", {}).get("byPath", {}).get("path") == "../SupplyChain360.SemanticModel",
        "definition.pbir must bind to ../SupplyChain360.SemanticModel",
    )

    pbism = load_json(MODEL / "definition.pbism")
    check(pbism.get("$schema") == PBISM_SCHEMA, "definition.pbism missing/incorrect required $schema")
    check(pbism.get("version") == "4.2", "definition.pbism version must be 4.2")

    version = load_json(REPORT_DEF / "version.json")
    check(version.get("$schema") == VERSION_SCHEMA, "version.json missing/incorrect $schema")
    check(version.get("version") == "2.0.0", "PBIR definition content version must be 2.0.0")

    report_meta = load_json(REPORT_DEF / "report.json")
    check(report_meta.get("$schema") == REPORT_SCHEMA, "report.json schema must be report/3.3.0")
    check(bool(report_meta.get("themeCollection")), "report.json must contain themeCollection")

    json_count = validate_json_tree(REPORT)

    pages_json = REPORT_DEF / "pages" / "pages.json"
    page_meta = load_json(pages_json)
    check(page_meta.get("$schema") == PAGES_SCHEMA, "pages.json schema must be pagesMetadata/1.1.0")
    page_order = page_meta.get("pageOrder") or []
    page_count = len(page_order)
    active_page = page_meta.get("activePageName")
    check(page_count == 14, f"Expected exactly 14 report pages; found {page_count}")
    check(active_page in page_order, "activePageName must reference a registered page")

    visual_count = 0
    visual_types: dict[str, int] = {}
    for page_id in page_order:
        check(bool(HEX20.fullmatch(page_id)), f"Desktop-unsafe page folder name: {page_id}")
        page_dir = REPORT_DEF / "pages" / page_id
        page_path = page_dir / "page.json"
        check(page_path.exists(), f"Registered report page missing: {page_id}")
        page = load_json(page_path)
        check(page.get("$schema") == PAGE_SCHEMA, f"Page {page_id} has unexpected schema")
        check(page.get("name") == page_id, f"Page name does not match folder: {page_id}")
        check(bool(page.get("displayName")), f"Page {page_id} missing displayName")
        check(bool(page.get("displayOption")), f"Page {page_id} missing displayOption")

        visuals_dir = page_dir / "visuals"
        if visuals_dir.exists():
            for visual_dir in sorted(p for p in visuals_dir.iterdir() if p.is_dir()):
                visual_id = visual_dir.name
                visual_count += 1
                check(bool(HEX20.fullmatch(visual_id)), f"Desktop-unsafe visual folder name: {visual_id}")
                visual_path = visual_dir / "visual.json"
                check(visual_path.exists(), f"Visual folder missing visual.json: {visual_dir.relative_to(ROOT)}")
                visual = load_json(visual_path)
                check(visual.get("$schema") == VISUAL_SCHEMA, f"Visual {visual_id} has unexpected schema")
                check(visual.get("name") == visual_id, f"Visual name does not match folder: {visual_id}")
                check(isinstance(visual.get("position"), dict), f"Visual {visual_id} missing position")
                if "visual" in visual:
                    vtype = visual.get("visual", {}).get("visualType")
                    check(bool(vtype), f"Visual {visual_id} missing visualType")
                    if vtype:
                        visual_types[vtype] = visual_types.get(vtype, 0) + 1

                    # sortDefinition belongs beside queryState under visual.query,
                    # never inside queryState. Desktop can fail to materialize the
                    # entire report exploration when this contract is violated.
                    query = visual.get("visual", {}).get("query", {})
                    query_state = query.get("queryState", {}) if isinstance(query, dict) else {}
                    check(
                        not (isinstance(query_state, dict) and "sortDefinition" in query_state),
                        f"Visual {visual_id} has invalid queryState.sortDefinition; move it to visual.query.sortDefinition",
                    )

    check(visual_count >= 250, f"Report visual count appears unexpectedly low: {visual_count}")
    check(visual_types.get("card", 0) == 0, "Legacy 'card' visuals detected; use cardVisual")
    check(visual_types.get("cardVisual", 0) > 0, "No modern cardVisual visuals detected")

    # Theme resource referenced by report.json should exist in source package.
    theme_items = report_meta.get("resourcePackages", [])
    for package in theme_items:
        for item in package.get("items", []):
            rel = item.get("path")
            if rel:
                theme_path = REPORT / "StaticResources" / "SharedResources" / rel
                check(theme_path.exists(), f"Referenced report resource missing: {theme_path.relative_to(ROOT)}")

    table_files = sorted(TABLES.glob("*.tmdl"))
    table_names = {p.stem for p in table_files}
    check(len(table_files) >= 14, f"Expected semantic tables including security table; found {len(table_files)}")

    model_text = read(MODEL_DEF / "model.tmdl")
    for param in ("ServerName", "DatabaseName", "EnvironmentName", "RangeStart", "RangeEnd"):
        check(f"expression {param}" in model_text, f"Missing model parameter: {param}")

    check("role Executive" in model_text, "Missing Executive RLS role")
    check("role 'Regional Manager'" in model_text, "Missing Regional Manager RLS role")
    check("USERPRINCIPALNAME()" in model_text, "Dynamic RLS must use USERPRINCIPALNAME()")
    check("ref table 'Security User Access'" in model_text, "Security mapping table is not referenced by model")

    hardcoded_source = []
    for tmdl in table_files:
        text = read(tmdl)
        if 'Sql.Database("localhost", "WideWorldImportersDW")' in text:
            hardcoded_source.append(tmdl.name)
    check(not hardcoded_source, f"Hard-coded SQL connection remains in: {hardcoded_source}")

    transactional = {
        "Fact Order Fulfillment.tmdl": "Order Date Key",
        "Fact Procurement.tmdl": "Date Key",
        "Fact Sales Demand.tmdl": "Invoice Date Key",
        "Fact Stock Movement.tmdl": "Date Key",
    }
    for filename, date_column in transactional.items():
        text = read(TABLES / filename)
        check("RangeStart" in text and "RangeEnd" in text, f"Range filter missing in {filename}")
        check(
            f'{{{{"{date_column}", type datetime}}}}' in text,
            f"{filename} must normalize {date_column} to DateTime before RangeStart/RangeEnd comparison",
        )

    relationships = read(MODEL_DEF / "relationships.tmdl")
    for table, column in re.findall(r"(?:fromColumn|toColumn): '([^']+)'\.'([^']+)'", relationships):
        check(table in table_names, f"Relationship references missing table: {table}")
        table_text = read(TABLES / f"{table}.tmdl")
        col_pattern = re.compile(rf"\n\tcolumn (?:'{re.escape(column)}'|{re.escape(column)})(?:\n|\t)")
        check(bool(col_pattern.search(table_text)), f"Relationship references missing column: {table}[{column}]")

    forbidden = list(ROOT.rglob("*.pbix")) + list(ROOT.rglob("*.pbit"))
    check(not forbidden, "PBIX/PBIT binaries should not be committed; use PBIP/PBIR/TMDL source")

    sql_views = list((ROOT / "sql" / "views").glob("*.sql"))
    sql_validations = list((ROOT / "sql" / "validation").glob("*.sql"))
    check(len(sql_views) >= 5, f"Expected >=5 SQL analytics views; found {len(sql_views)}")
    check(len(sql_validations) >= 7, f"Expected >=7 SQL validation scripts; found {len(sql_validations)}")
    check((ROOT / "sql" / "setup" / "00_install_analytics_layer.sql").exists(), "Missing one-shot analytics-layer installer")

    gitignore = read(ROOT / ".gitignore")
    check(".pbi" in gitignore, ".gitignore should exclude local Power BI cache/settings")

    measures = read(TABLES / "_Measures.tmdl")
    measure_count = len(re.findall(r"\n\tmeasure ", measures))
    check(measure_count >= 100, f"Measure layer appears unexpectedly small: {measure_count} measures")

    print("SupplyChain360 Desktop-strict quality gate")
    print(f"  PBIR JSON files : {json_count}")
    print(f"  Report pages    : {page_count}")
    print(f"  Report visuals  : {visual_count}")
    print(f"  Visual types    : {len(visual_types)}")
    print(f"  TMDL tables     : {len(table_files)}")
    print(f"  DAX measures    : {measure_count}")
    print(f"  SQL views       : {len(sql_views)}")
    print(f"  SQL validations : {len(sql_validations)}")

    for warning in WARNINGS:
        print(f"WARNING: {warning}")

    if ERRORS:
        print("\nQUALITY GATE: FAIL")
        for error in ERRORS:
            print(f" - {error}")
        return 1

    print("\nQUALITY GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
