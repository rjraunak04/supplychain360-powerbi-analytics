$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ReportRoot = Join-Path $RepoRoot "powerbi\SupplyChain360.Report"
$SemanticRoot = Join-Path $RepoRoot "powerbi\SupplyChain360.SemanticModel"
$Pbip = Join-Path $RepoRoot "powerbi\SupplyChain360.pbip"

Write-Host "SupplyChain360 PBIP runtime reset" -ForegroundColor Cyan
Write-Host "Repo: $RepoRoot"

$required = @(
    $Pbip,
    (Join-Path $ReportRoot "definition.pbir"),
    (Join-Path $ReportRoot "definition\pages\pages.json"),
    (Join-Path $SemanticRoot "definition.pbism")
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        throw "Missing required project file: $path"
    }
}

$pages = Get-Content (Join-Path $ReportRoot "definition\pages\pages.json") -Raw | ConvertFrom-Json
$pageCount = @($pages.pageOrder).Count
Write-Host "Registered report pages: $pageCount"

if ($pageCount -lt 14) {
    throw "Expected 14 report pages but found $pageCount"
}

$missingPages = @()
foreach ($pageId in $pages.pageOrder) {
    $pageJson = Join-Path $ReportRoot "definition\pages\$pageId\page.json"
    if (-not (Test-Path $pageJson)) {
        $missingPages += $pageId
    }
}

if ($missingPages.Count -gt 0) {
    throw "Missing page definitions: $($missingPages -join ', ')"
}

Write-Host "All page definitions present." -ForegroundColor Green

# Power BI project cache is local-only and can preserve a stale/blank runtime state
# after model/report files change outside Desktop.
$cacheDirs = @(
    (Join-Path $ReportRoot ".pbi"),
    (Join-Path $SemanticRoot ".pbi"),
    (Join-Path $RepoRoot "powerbi\.pbi")
)

foreach ($dir in $cacheDirs) {
    if (Test-Path $dir) {
        Write-Host "Removing stale local cache: $dir"
        Remove-Item $dir -Recurse -Force
    }
}

Write-Host ""
Write-Host "PBIP source is intact and local Power BI cache was reset." -ForegroundColor Green
Write-Host "Now open only:"
Write-Host $Pbip -ForegroundColor Yellow
