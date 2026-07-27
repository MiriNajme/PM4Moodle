# Prepares the Moodle source for the Docker demo (Windows).
#
#   powershell -ExecutionPolicy Bypass -File docker\prepare-moodle.ps1
#
# Why this exists: the Moodle code folder holds ~29,000 files. Copying those
# individually across Docker's Windows file-sharing boundary takes 30+ minutes.
# Packing them into a single tarball here (native disk access, fast) lets the
# container extract it internally in a couple of minutes instead.
#
# Reads MOODLE_SRC from .env unless -Source is given.

param(
    [string]$Source,
    [string]$OutFile
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

if (-not $Source) {
    $envFile = Join-Path $repoRoot '.env'
    if (Test-Path $envFile) {
        foreach ($line in Get-Content $envFile) {
            if ($line -match '^\s*MOODLE_SRC\s*=\s*(.+?)\s*$') { $Source = $Matches[1] }
        }
    }
}

if (-not $Source) {
    Write-Error "MOODLE_SRC not set. Add it to .env or pass -Source <path>."
}

if (-not (Test-Path (Join-Path $Source 'version.php'))) {
    Write-Error "'$Source' does not look like a Moodle code folder (no version.php)."
}

$distDir = Join-Path $PSScriptRoot 'moodle-dist'
if (-not (Test-Path $distDir)) { New-Item -ItemType Directory -Path $distDir | Out-Null }
if (-not $OutFile) { $OutFile = Join-Path $distDir 'moodle-src.tar.gz' }

$release = (Select-String -Path (Join-Path $Source 'version.php') -Pattern "\`$release\s*=\s*'([^']+)'").Matches.Groups[1].Value
Write-Host "Packing Moodle source..." -ForegroundColor Cyan
Write-Host "  source : $Source"
Write-Host "  release: $release"
Write-Host "  output : $OutFile"
Write-Host "This takes a minute or two." -ForegroundColor Yellow

# bsdtar ships with Windows 10+ as tar.exe.
& tar.exe --exclude='.git' -czf $OutFile -C $Source .
if ($LASTEXITCODE -ne 0) { Write-Error "tar failed with exit code $LASTEXITCODE" }

$sizeMb = [math]::Round((Get-Item $OutFile).Length / 1MB, 1)
Write-Host "Done: $OutFile ($sizeMb MB)" -ForegroundColor Green
Write-Host ""
Write-Host "Now start the full demo with:" -ForegroundColor Cyan
Write-Host "  docker compose -f docker-compose.yml -f docker-compose.moodle.yml up -d"
