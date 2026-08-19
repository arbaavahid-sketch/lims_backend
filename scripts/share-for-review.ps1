# share-for-review.ps1
# Opens a TEMPORARY public HTTPS link so remote managers can review the LIMS,
# even on a filtered network where Cloudflare tunnels are blocked.
#
# Chain:  serveo.net (public HTTPS)  ->  Caddy (fixes Zope https links)  ->  SENAITE :8080
#
# Notes:
#   - The link is temporary and CHANGES every run (free serveo).
#   - Keep this window OPEN during the review; closing it stops the link.
#   - HTTPS is provided by serveo, so logins are encrypted.
#   - First visit may show a serveo warning page -> click "Continue".
#
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\share-for-review.ps1

$ErrorActionPreference = "Stop"
$here      = Split-Path -Parent $MyInvocation.MyCommand.Path
$caddyfile = Join-Path $here "Caddyfile"
$network   = "lims_backend_default"   # docker network of the senaite container

if (-not (Test-Path $caddyfile)) { throw "Caddyfile not found next to this script: $caddyfile" }

Write-Host "[1/2] Starting the Caddy proxy (fixes https links for SENAITE)..." -ForegroundColor Cyan
docker rm -f tandis-caddy 2>$null | Out-Null
docker run -d --name tandis-caddy --network $network -p 9080:9080 `
    -v "${caddyfile}:/etc/caddy/Caddyfile" caddy:2 | Out-Null
Write-Host "      Caddy is up on http://localhost:9080" -ForegroundColor Green

Write-Host ""
Write-Host "[2/2] Opening the public link (serveo). Look for the https://...serveo... URL below." -ForegroundColor Cyan
Write-Host "      Send that URL + '/senaite/' to the managers. Keep THIS window open." -ForegroundColor Yellow
Write-Host "      Press Ctrl+C here to stop sharing." -ForegroundColor Yellow
Write-Host ""

# Foreground SSH tunnel: prints the public URL and stays open until you close it.
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL -o ServerAliveInterval=30 `
    -o ExitOnForwardFailure=yes -R 80:localhost:9080 serveo.net

# When SSH exits (Ctrl+C / window closed), tidy up the proxy.
Write-Host ""
Write-Host "Link closed. Stopping the Caddy proxy..." -ForegroundColor Cyan
docker rm -f tandis-caddy 2>$null | Out-Null
Write-Host "Done. Sharing stopped." -ForegroundColor Green
