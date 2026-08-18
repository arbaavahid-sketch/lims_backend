# backup.ps1 - automated backup of the SENAITE data volume (senaite_data)
# Run:  powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
# Schedule daily via Windows Task Scheduler (see docs/RUNBOOK.md).
#
# Creates a timestamped tar.gz in the backups folder and keeps only the last
# -KeepDays copies (rotation).

param(
    [int]$KeepDays = 14,
    [string]$Volume = "senaite_data",
    [string]$Prefix = "senaite-data"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backupDir = Join-Path $root "backups"
if (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }

$stamp = Get-Date -Format "yyyyMMdd-HHmm"
$name  = "$Prefix-$stamp.tar.gz"
$dockerBackupPath = ($backupDir -replace '\\','/')

Write-Host "[backup] creating $name ..."
docker run --rm -v "${Volume}:/data" -v "${dockerBackupPath}:/backup" alpine `
    tar czf "/backup/$name" -C /data .

$file = Join-Path $backupDir $name
if (-not (Test-Path $file)) { throw "backup not created: $file" }
$sizeMB = [math]::Round((Get-Item $file).Length / 1MB, 1)
Write-Host ("[backup] created: {0} ({1} MB)" -f $name, $sizeMB)

# Rotation: keep only the most recent $KeepDays files
$all = Get-ChildItem $backupDir -Filter "$Prefix-*.tar.gz" | Sort-Object LastWriteTime -Descending
if ($all.Count -gt $KeepDays) {
    $all | Select-Object -Skip $KeepDays | ForEach-Object {
        Write-Host ("[backup] removing old: {0}" -f $_.Name)
        Remove-Item $_.FullName -Force
    }
}
Write-Host ("[backup] done. copies kept: {0}" -f [math]::Min($all.Count, $KeepDays))
