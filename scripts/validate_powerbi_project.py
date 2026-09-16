#!/usr/bin/env python3
"""Static quality gate for the SupplyChain360 PBIP/PBIR/TMDL project.

Uses only the Python standard library so it can run locally and in GitHub Actions.
It validates repository structure, PBIR JSON, semantic-model references,
environment parameterization, RLS metadata, SQL assets and accidental binaries.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POWERBI = ROOT / "powerbi"
REPORT = POWERBI / "SupplyChain360.Report"
MODEL = POWERBI / "SupplyChain360.SemanticModel"
DEFINITION = MODEL / "definition"
TABLES = DEFINITION / "tables"
ERRORS: list[str] = []
WARNINGS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        ERRORS.append(f"Cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


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
        POWERBI / "SupplyChain360.pbip",
        REPORT / "definition.pbir",
        MODEL / "definition.pbism",
        DEFINITION / "model.tmdl",
        DEFINITION / "relationships.tmdl",
        TABLES / "_Measures.tmdl",
        TABLES / "Security User Access.tmdl",
        ROOT / "README.md",
        ROOT / ".gitignore",
    ]
    for path in required:
        check(path.exists(), f"Missing required asset: {path.relative_to(ROOT)}")

    json_count = validate_json_tree(REPORT)

    pages_json = REPORT / "definition" / "pages" / "pages.json"
    page_count = 0
    if pages_json.exists():
        try:
            page_meta = json.loads(read(pages_json))
            page_order = page_meta.get("pageOrder", [])
            page_count = len(page_order)
            check(page_count >= 14, f"Expected at least 14 report pages; found {page_count}")
            for page_id in page_order:
                check(
                    (REPORT / "definition" / "pages" / page_id / "page.json").exists(),
                    f"Registered report page missing: {page_id}",
                )
        except Exception as exc:
            ERRORS.append(f"Cannot validate pages.json: {exc}")

    table_files = sorted(TABLES.glob("*.tmdl"))
    table_names = {p.stem for p in table_files}
    check(len(table_files) >= 14, f"Expected semantic tables including security table; found {len(table_files)}")

    model_text = read(DEFINITION / "model.tmdl")
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
        "Fact Order Fulfillment.tmdl": "RangeStart",
        "Fact Procurement.tmdl": "RangeStart",
        "Fact Sales Demand.tmdl": "RangeStart",
        "Fact Stock Movement.tmdl": "RangeStart",
    }
    for filename, marker in transactional.items():
        text = read(TABLES / filename)
        check(marker in text and "RangeEnd" in text, f"Incremental-range filter missing in {filename}")

    # Basic relationship reference validation.
    relationships = read(DEFINITION / "relationships.tmdl")
    for table, column in re.findall(r"(?:fromColumn|toColumn): '([^']+)'\.'([^']+)'", relationships):
        check(table in table_names, f"Relationship references missing table: {table}")
        table_text = read(TABLES / f"{table}.tmdl")
        col_pattern = re.compile(rf"\n\tcolumn (?:'{re.escape(column)}'|{re.escape(column)})(?:\n|\t)")
        check(bool(col_pattern.search(table_text)), f"Relationship references missing column: {table}[{column}]")

    # Guard against committing large binary PBIX/PBIT artifacts.
    forbidden = list(ROOT.rglob("*.pbix")) + list(ROOT.rglob("*.pbit"))
    check(not forbidden, "PBIX/PBIT binary files should not be committed; use PBIP/PBIR/TMDL source")

    sql_views = list((ROOT / "sql" / "views").glob("*.sql"))
    sql_validations = list((ROOT / "sql" / "validation").glob("*.sql"))
    check(len(sql_views) >= 5, f"Expected >=5 SQL analytics views; found {len(sql_views)}")
    check(len(sql_validations) >= 7, f"Expected >=7 SQL validation scripts; found {len(sql_validations)}")

    gitignore = read(ROOT / ".gitignore")
    check(".pbi" in gitignore, ".gitignore should exclude local Power BI cache/settings")

    measures = read(TABLES / "_Measures.tmdl")
    measure_count = len(re.findall(r"\n\tmeasure ", measures))
    check(measure_count >= 80, f"Measure layer appears unexpectedly small: {measure_count} measures")

    print("SupplyChain360 static quality gate")
    print(f"  PBIR JSON files : {json_count}")
    print(f"  Report pages    : {page_count}")
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
