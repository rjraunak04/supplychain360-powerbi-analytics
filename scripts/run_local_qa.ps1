$ErrorActionPreference = "Stop"

Write-Host "SupplyChain360 Local QA" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Python static quality gate"
python .\scripts\validate_powerbi_project.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[2/4] Git working tree"
git status --short
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[3/4] Large binary guard"
$bad = Get-ChildItem -Recurse -File -Include *.pbix,*.pbit -ErrorAction SilentlyContinue
if ($bad) {
    Write-Error "PBIX/PBIT binaries found. Keep PBIP/PBIR/TMDL source in Git."
    $bad | ForEach-Object { Write-Host $_.FullName }
    exit 1
}
Write-Host "No PBIX/PBIT binaries found."

Write-Host ""
Write-Host "[4/4] Optional SQL connectivity"
$sqlcmd = Get-Command sqlcmd -ErrorAction SilentlyContinue
if ($sqlcmd) {
    sqlcmd -S localhost -d WideWorldImportersDW -E -Q "SELECT DB_NAME() AS DatabaseName, @@SERVERNAME AS ServerName;"
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "SQL connectivity check failed. Verify SQL Server is running in multi-user mode."
    }
}
else {
    Write-Host "sqlcmd not installed; skipped SQL connectivity check."
}

Write-Host ""
Write-Host "STATIC LOCAL QA COMPLETE." -ForegroundColor Green
Write-Host "Next manual gate: open powerbi\SupplyChain360.pbip and run Refresh All."
