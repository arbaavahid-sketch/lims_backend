# restore.ps1 - restore SENAITE data from a backup file
# Drill (into a TEST volume, safe):
#   powershell -ExecutionPolicy Bypass -File scripts\restore.ps1 -BackupFile backups\senaite-data-XXXX.tar.gz -TargetVolume senaite_data_restore_test
# Real restore (overwrites live data - stop the container first, back up first):
#   powershell -ExecutionPolicy Bypass -File scripts\restore.ps1 -BackupFile backups\senaite-data-XXXX.tar.gz -TargetVolume senaite_data -Confirm

param(
    [Parameter(Mandatory=$true)][string]$BackupFile,
    [string]$TargetVolume = "senaite_data_restore_test",
    [switch]$Confirm
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

if (-not [System.IO.Path]::IsPathRooted($BackupFile)) {
    $BackupFile = Join-Path $root $BackupFile
}
if (-not (Test-Path $BackupFile)) { throw "backup file not found: $BackupFile" }

if ($TargetVolume -eq "senaite_data" -and -not $Confirm) {
    throw "Restoring onto the live 'senaite_data' volume needs -Confirm (it overwrites current data)."
}

$exists = docker volume ls --format "{{.Name}}" | Select-String -SimpleMatch $TargetVolume
if (-not $exists) {
    Write-Host "[restore] creating volume: $TargetVolume"
    docker volume create $TargetVolume | Out-Null
}

$backupFull = (Resolve-Path $BackupFile).Path
$dir = Split-Path -Parent $backupFull
$file = Split-Path -Leaf $backupFull
$dockerDir = ($dir -replace '\\','/')

Write-Host "[restore] restoring '$file' -> volume '$TargetVolume' ..."
docker run --rm -v "${TargetVolume}:/data" -v "${dockerDir}:/backup" alpine `
    sh -c "rm -rf /data/* /data/..?* /data/.[!.]* 2>/dev/null; tar xzf /backup/$file -C /data; echo '[restore] data size:'; du -sh /data"

Write-Host "[restore] done. target volume: $TargetVolume"
