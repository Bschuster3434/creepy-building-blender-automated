# Run Iteration Script
# Executes one complete iteration of the geometry generation pipeline

param(
    [switch]$WhatIf,  # Dry run mode
    [switch]$Verbose  # Verbose output
)

$ErrorActionPreference = "Stop"

# --- Configuration Loading ---

function Load-Config {
    $configPath = Join-Path $PSScriptRoot "..\config\local.env"
    $examplePath = Join-Path $PSScriptRoot "..\config\local.env.example"

    if (-not (Test-Path $configPath)) {
        Write-Host "ERROR: Configuration file not found: $configPath" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please copy the example configuration:" -ForegroundColor Yellow
        Write-Host "  copy `"$examplePath`" `"$configPath`"" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Then edit $configPath and set BLENDER_PATH to your Blender executable." -ForegroundColor Yellow
        exit 1
    }

    $config = @{}
    Get-Content $configPath | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $config[$key] = $value
        }
    }

    # Validate required config
    if (-not $config.ContainsKey("BLENDER_PATH") -or [string]::IsNullOrWhiteSpace($config["BLENDER_PATH"])) {
        Write-Host "ERROR: BLENDER_PATH not set in $configPath" -ForegroundColor Red
        exit 1
    }

    if (-not (Test-Path $config["BLENDER_PATH"])) {
        Write-Host "ERROR: Blender not found at: $($config['BLENDER_PATH'])" -ForegroundColor Red
        Write-Host "Please update BLENDER_PATH in $configPath" -ForegroundColor Yellow
        exit 1
    }

    return $config
}

# --- Version/Iteration Detection ---

function Get-LatestSpecVersion {
    $specDir = Join-Path $PSScriptRoot "..\work\spec"

    if (-not (Test-Path $specDir)) {
        Write-Host "ERROR: Spec directory not found: $specDir" -ForegroundColor Red
        exit 1
    }

    $specs = Get-ChildItem -Path $specDir -Filter "building_v*.yaml" -ErrorAction SilentlyContinue

    if ($specs.Count -eq 0) {
        Write-Host "ERROR: No spec files found in $specDir" -ForegroundColor Red
        Write-Host "Please create a spec file (e.g., building_v001.yaml)" -ForegroundColor Yellow
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

function Get-NextIterationNumber {
    $rendersDir = Join-Path $PSScriptRoot "..\work\renders"

    if (-not (Test-Path $rendersDir)) {
        return 1
    }

    $iters = Get-ChildItem -Path $rendersDir -Directory -Filter "iter_*" -ErrorAction SilentlyContinue

    if ($iters.Count -eq 0) {
        return 1
    }

    $numbers = $iters | ForEach-Object {
        if ($_.Name -match 'iter_(\d+)') {
            [int]$matches[1]
        }
    } | Sort-Object -Descending

    return $numbers[0] + 1
}

# --- Main Script ---

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Pipeline Iteration Runner" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Load configuration
$config = Load-Config
Write-Host "[Config] Loaded from config\local.env" -ForegroundColor Green

# Get latest spec
$latestSpec = Get-LatestSpecVersion
Write-Host "[Spec]   Using $($latestSpec.Name) (version $($latestSpec.Version))" -ForegroundColor Green

# Get next iteration number
$nextIter = Get-NextIterationNumber
$iterFormatted = "iter_{0:D3}" -f $nextIter
Write-Host "[Iter]   Next iteration: $iterFormatted (#$nextIter)" -ForegroundColor Green

# Define output paths
$rootDir = Split-Path -Parent $PSScriptRoot
$glbOutput = Join-Path $rootDir "exports\glb\building_$iterFormatted.glb"
$rendersDir = Join-Path $rootDir "work\renders\$iterFormatted"
$metricsJson = Join-Path $rootDir "work\metrics\metrics_$("{0:D3}" -f $nextIter).json"
$logDir = Join-Path $rootDir "work\logs\$iterFormatted"
$logFile = Join-Path $logDir "run.log"

Write-Host ""
Write-Host "Output paths:" -ForegroundColor Yellow
Write-Host "  GLB:     $glbOutput" -ForegroundColor Gray
Write-Host "  Renders: $rendersDir" -ForegroundColor Gray
Write-Host "  Metrics: $metricsJson" -ForegroundColor Gray
Write-Host "  Log:     $logFile" -ForegroundColor Gray
Write-Host ""

if ($WhatIf) {
    Write-Host "[WHATIF] Dry run mode - no actions performed" -ForegroundColor Magenta
    exit 0
}

# Create output directories
New-Item -ItemType Directory -Force -Path (Split-Path $glbOutput) | Out-Null
New-Item -ItemType Directory -Force -Path $rendersDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $metricsJson) | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

# Start logging
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "=== Pipeline Iteration $iterFormatted ==="
Add-Content -Path $logFile -Value "Timestamp: $timestamp"
Add-Content -Path $logFile -Value "Spec: $($latestSpec.Name)"
Add-Content -Path $logFile -Value ""

# --- Stage 1: Blender Geometry Generation ---

Write-Host "[Stage 1] Running Blender geometry generation..." -ForegroundColor Cyan

$blenderScript = Join-Path $PSScriptRoot "blender\build_from_spec.py"
$blenderArgs = @(
    "-b",  # Background mode (headless)
    "-P", $blenderScript,
    "--",  # Separator for script arguments
    "--spec", $latestSpec.Path,
    "--out_glb", $glbOutput,
    "--out_renders_dir", $rendersDir,
    "--out_metrics_json", $metricsJson
)

Add-Content -Path $logFile -Value "Blender command:"
Add-Content -Path $logFile -Value "`"$($config['BLENDER_PATH'])`" $($blenderArgs -join ' ')"
Add-Content -Path $logFile -Value ""

try {
    Write-Host "  Executing Blender (this may take a while)..." -ForegroundColor Gray

    # TODO: Capture stdout and stderr separately
    # TODO: Stream output to console in real-time if -Verbose
    # TODO: Handle Blender exit codes properly

    $process = Start-Process -FilePath $config["BLENDER_PATH"] `
                             -ArgumentList $blenderArgs `
                             -NoNewWindow `
                             -Wait `
                             -PassThru `
                             -RedirectStandardOutput (Join-Path $logDir "blender_stdout.log") `
                             -RedirectStandardError (Join-Path $logDir "blender_stderr.log")

    $exitCode = $process.ExitCode
    Add-Content -Path $logFile -Value "Blender exit code: $exitCode"

    if ($exitCode -ne 0) {
        Write-Host "  WARNING: Blender exited with code $exitCode" -ForegroundColor Yellow
        Write-Host "  Check logs: $logDir" -ForegroundColor Yellow
    } else {
        Write-Host "  Blender completed successfully" -ForegroundColor Green
    }

} catch {
    Write-Host "  ERROR: Blender execution failed" -ForegroundColor Red
    Write-Host "  $_" -ForegroundColor Red
    Add-Content -Path $logFile -Value "ERROR: $_"
    exit 1
}

Write-Host ""

# --- Stage 2: Validation (Optional) ---

Write-Host "[Stage 2] Validating geometry metrics..." -ForegroundColor Cyan

if (Test-Path $metricsJson) {
    $validatorScript = Join-Path $PSScriptRoot "validate_geometry.py"

    # TODO: Check if Python is available
    # TODO: Use PYTHON from config if specified

    try {
        $pythonCmd = if ($config.ContainsKey("PYTHON") -and -not [string]::IsNullOrWhiteSpace($config["PYTHON"])) {
            $config["PYTHON"]
        } else {
            "python"
        }

        Write-Host "  Running validator..." -ForegroundColor Gray
        & $pythonCmd $validatorScript --metrics $metricsJson

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Validation passed" -ForegroundColor Green
        } else {
            Write-Host "  Validation warnings/errors detected" -ForegroundColor Yellow
        }

    } catch {
        Write-Host "  WARNING: Could not run validator (Python may not be available)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  WARNING: Metrics file not found, skipping validation" -ForegroundColor Yellow
}

Write-Host ""

# --- Stage 3: TODO - Critique Generation ---

Write-Host "[Stage 3] TODO: Critique generation not implemented" -ForegroundColor Yellow
Write-Host "  Next steps:" -ForegroundColor Gray
Write-Host "    1. Review renders in: $rendersDir" -ForegroundColor Gray
Write-Host "    2. Compare with references in: inputs\reference" -ForegroundColor Gray
Write-Host "    3. Generate critique JSON (manual or AI)" -ForegroundColor Gray
Write-Host "    4. Save to: work\reviews\critique_$("{0:D3}" -f $nextIter).json" -ForegroundColor Gray

Write-Host ""

# --- Stage 4: TODO - Spec Editing ---

Write-Host "[Stage 4] TODO: Spec editing not implemented" -ForegroundColor Yellow
Write-Host "  Next steps:" -ForegroundColor Gray
Write-Host "    1. Load critique JSON" -ForegroundColor Gray
Write-Host "    2. Apply fixes to spec (manual or AI)" -ForegroundColor Gray
Write-Host "    3. Use scripts\new_iteration.ps1 to version the spec" -ForegroundColor Gray

Write-Host ""

# --- Summary ---

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Iteration $iterFormatted Complete" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Outputs:" -ForegroundColor Green
Write-Host "  GLB:     $glbOutput" -ForegroundColor Gray
Write-Host "  Renders: $rendersDir" -ForegroundColor Gray
Write-Host "  Metrics: $metricsJson" -ForegroundColor Gray
Write-Host "  Logs:    $logDir" -ForegroundColor Gray
Write-Host ""

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value ""
Add-Content -Path $logFile -Value "Completed: $endTimestamp"

exit 0
