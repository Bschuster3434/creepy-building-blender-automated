# New Iteration Script
# Creates a new version of the building spec by copying the latest version

param(
    [string]$Message = "",  # Optional change message
    [switch]$WhatIf         # Dry run mode
)

$ErrorActionPreference = "Stop"

# --- Helper Functions ---

function Get-LatestSpec {
    $specDir = Join-Path $PSScriptRoot "..\work\spec"

    if (-not (Test-Path $specDir)) {
        Write-Host "ERROR: Spec directory not found: $specDir" -ForegroundColor Red
        exit 1
    }

    $specs = Get-ChildItem -Path $specDir -Filter "building_v*.yaml" -ErrorAction SilentlyContinue

    if ($specs.Count -eq 0) {
        Write-Host "ERROR: No spec files found in $specDir" -ForegroundColor Red
        exit 1
    }

    $versions = $specs | ForEach-Object {
        if ($_.Name -match 'building_v(\d+)\.yaml') {
            [PSCustomObject]@{
                Version = [int]$matches[1]
                Path = $_.FullName
                Name = $_.Name
            }
        }
    } | Sort-Object -Property Version -Descending

    return $versions[0]
}

function Format-YamlComment {
    param([string]$text)
    return "# $text"
}

# --- Main Script ---

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  New Spec Version Creator" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Get latest spec
$latestSpec = Get-LatestSpec
$currentVersion = $latestSpec.Version
$nextVersion = $currentVersion + 1

$currentName = $latestSpec.Name
$nextName = "building_v{0:D3}.yaml" -f $nextVersion

$specDir = Join-Path $PSScriptRoot "..\work\spec"
$nextPath = Join-Path $specDir $nextName

Write-Host "Current spec: $currentName (v$currentVersion)" -ForegroundColor Green
Write-Host "New spec:     $nextName (v$nextVersion)" -ForegroundColor Green
Write-Host ""

# Check if next version already exists
if (Test-Path $nextPath) {
    Write-Host "ERROR: Next version already exists: $nextPath" -ForegroundColor Red
    Write-Host "Delete it first or use a different version number." -ForegroundColor Yellow
    exit 1
}

# Get change message
if ([string]::IsNullOrWhiteSpace($Message)) {
    Write-Host "Enter change message (or press Enter for default):" -ForegroundColor Yellow
    $userInput = Read-Host
    if (-not [string]::IsNullOrWhiteSpace($userInput)) {
        $Message = $userInput
    } else {
        $Message = "New iteration from v{0:D3}" -f $currentVersion
    }
}

Write-Host ""
Write-Host "Change message: $Message" -ForegroundColor Cyan
Write-Host ""

if ($WhatIf) {
    Write-Host "[WHATIF] Would create: $nextPath" -ForegroundColor Magenta
    Write-Host "[WHATIF] Would copy from: $($latestSpec.Path)" -ForegroundColor Magenta
    exit 0
}

# Read current spec
$specContent = Get-Content -Path $latestSpec.Path -Raw

# Create header comment
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$header = @"
# Updated: $timestamp
# Previous version: v{0:D3}
# Changes: $Message
# Version: v{0:D3} -> v{1:D3}
#
"@ -f $currentVersion, $nextVersion

# Check if spec already has a version field and update it
if ($specContent -match '(?m)^version:\s*v\d+') {
    $newVersionLine = "version: v{0:D3}" -f $nextVersion
    $specContent = $specContent -replace '(?m)^version:\s*v\d+', $newVersionLine
} else {
    # Add version field after header if not present
    Write-Host "WARNING: No version field found in spec, adding it" -ForegroundColor Yellow
}

# Combine header and content
$newContent = $header + $specContent

# Write new spec file
try {
    Set-Content -Path $nextPath -Value $newContent -NoNewline
    Write-Host "Successfully created: $nextPath" -ForegroundColor Green
    Write-Host ""

    # Show diff summary
    Write-Host "Summary:" -ForegroundColor Yellow
    Write-Host "  Previous: $($latestSpec.Path)" -ForegroundColor Gray
    Write-Host "  New:      $nextPath" -ForegroundColor Gray
    Write-Host "  Message:  $Message" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Edit the new spec file: $nextPath" -ForegroundColor Gray
    Write-Host "  2. Make your changes based on critique or manual review" -ForegroundColor Gray
    Write-Host "  3. Run: .\scripts\run_iteration.ps1" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host "ERROR: Failed to create new spec file" -ForegroundColor Red
    Write-Host "$_" -ForegroundColor Red
    exit 1
}

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Spec Version Created Successfully" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

exit 0
