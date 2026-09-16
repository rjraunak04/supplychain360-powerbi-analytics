param(
    [switch]$NoOpen
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PowerBIRoot = Join-Path $RepoRoot "powerbi"
$Pbip = Join-Path $PowerBIRoot "SupplyChain360.pbip"
$ReportRoot = Join-Path $PowerBIRoot "SupplyChain360.Report"
$Pbir = Join-Path $ReportRoot "definition.pbir"
$ModelRoot = Join-Path $PowerBIRoot "SupplyChain360.SemanticModel"
$Pbism = Join-Path $ModelRoot "definition.pbism"
$PagesJson = Join-Path $ReportRoot "definition\pages\pages.json"

Write-Host ""
Write-Host "SupplyChain360 FINAL PBIR runtime repair" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Stop stale Desktop process so it cannot hold/cache an older project snapshot.
$desktop = Get-Process PBIDesktop -ErrorAction SilentlyContinue
if ($desktop) {
    Write-Host "Closing stale Power BI Desktop process..." -ForegroundColor Yellow
    $desktop | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# 2. Run the repository's Desktop-strict static validator.
Write-Host "[1/4] Desktop-strict project validation"
python (Join-Path $PSScriptRoot "validate_powerbi_project.py")
if ($LASTEXITCODE -ne 0) {
    throw "Static PBIP/PBIR/TMDL validation failed. Do not open/save the report."
}

# 3. Explicitly verify required schema metadata.
Write-Host "[2/4] Required project/report schema metadata"
$pbipObj = Get-Content $Pbip -Raw | ConvertFrom-Json
$pbirObj = Get-Content $Pbir -Raw | ConvertFrom-Json
$pbismObj = Get-Content $Pbism -Raw | ConvertFrom-Json

$expectedPbipSchema = "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json"
$expectedPbirSchema = "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json"
$expectedPbismSchema = "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json"

if ($pbipObj.'$schema' -ne $expectedPbipSchema) { throw "PBIP schema metadata is invalid." }
if ($pbirObj.'$schema' -ne $expectedPbirSchema) { throw "PBIR schema metadata is invalid." }
if ($pbismObj.'$schema' -ne $expectedPbismSchema) { throw "PBISM schema metadata is invalid." }

Write-Host "Required schema metadata: PASS" -ForegroundColor Green

# 4. Confirm all 14 page folders and visual files exist.
Write-Host "[3/4] Report exploration/page integrity"
$pages = Get-Content $PagesJson -Raw | ConvertFrom-Json
if (@($pages.pageOrder).Count -ne 14) {
    throw "Expected 14 report pages; found $(@($pages.pageOrder).Count)."
}
if ($pages.activePageName -notin $pages.pageOrder) {
    throw "activePageName is not registered in pageOrder."
}

$visualCount = 0
foreach ($pageId in $pages.pageOrder) {
    $pageDir = Join-Path $ReportRoot "definition\pages\$pageId"
    $pageJson = Join-Path $pageDir "page.json"
    if (-not (Test-Path $pageJson)) { throw "Missing page.json: $pageId" }

    $visualDir = Join-Path $pageDir "visuals"
    if (Test-Path $visualDir) {
        $visualCount += @(Get-ChildItem $visualDir -Directory | Where-Object {
            Test-Path (Join-Path $_.FullName "visual.json")
        }).Count
    }
}

if ($visualCount -lt 250) {
    throw "Report visual count is unexpectedly low: $visualCount"
}

Write-Host "Pages: 14 | Visuals: $visualCount | PASS" -ForegroundColor Green

# 5. Remove local-only Power BI caches. Source definitions remain untouched.
Write-Host "[4/4] Clearing local Power BI runtime caches"
$cacheDirs = @(
    (Join-Path $ReportRoot ".pbi"),
    (Join-Path $ModelRoot ".pbi"),
    (Join-Path $PowerBIRoot ".pbi")
)
foreach ($dir in $cacheDirs) {
    if (Test-Path $dir) {
        Remove-Item $dir -Recurse -Force
        Write-Host "Removed: $dir"
    }
}

Write-Host ""
Write-Host "FINAL STATIC/RUNTIME-SCAFFOLD CHECK: PASS" -ForegroundColor Green
Write-Host "Opening the report definition directly (bypasses PBIP shortcut caching):" -ForegroundColor Cyan
Write-Host $Pbir -ForegroundColor Yellow

if (-not $NoOpen) {
    Start-Process $Pbir
}
