# Naming Conventions

This document defines the file and directory naming standards for the pipeline.

## Version Numbers vs Iteration Numbers

### Version Numbers (Specs)
- **Format:** `v###` (e.g., `v001`, `v023`, `v142`)
- **Used for:** YAML specification files
- **Increments when:** Spec content changes (manual edit or AI edit)
- **Zero-padded:** Always 3 digits

### Iteration Numbers (Builds)
- **Format:** `iter_###` (e.g., `iter_001`, `iter_042`)
- **Used for:** Geometry builds, renders, metrics, reviews
- **Increments when:** New geometry build is executed
- **Zero-padded:** Always 3 digits

### Relationship
- One spec version can produce multiple iterations (e.g., fixing Blender script bugs)
- Each iteration references which spec version it used
- Spec versions track conceptual changes
- Iteration numbers track execution runs

## File Naming Patterns

### Specification Files
```
work/spec/building_v001.yaml
work/spec/building_v002.yaml
work/spec/building_v023.yaml
```

**Pattern:** `building_v###.yaml`
- Prefix: `building_` (fixed)
- Version: `v###` (3-digit zero-padded)
- Extension: `.yaml`

### GLB Exports
```
exports/glb/building_iter_001.glb
exports/glb/building_iter_002.glb
exports/glb/building_iter_042.glb
```

**Pattern:** `building_iter_###.glb`
- Prefix: `building_` (fixed)
- Iteration: `iter_###` (3-digit zero-padded)
- Extension: `.glb`

### Render Directories
```
work/renders/iter_001/
work/renders/iter_002/
work/renders/iter_042/
```

**Pattern:** `iter_###/`
- Iteration: `iter_###` (3-digit zero-padded)

### Render Files
```
work/renders/iter_001/front.png
work/renders/iter_001/left.png
work/renders/iter_001/right.png
work/renders/iter_001/rear.png
work/renders/iter_001/iso.png
work/renders/iter_001/top.png
```

**Pattern:** `{view}.png`
- Views: `front`, `left`, `right`, `rear`, `iso`, `top` (fixed names)
- Extension: `.png`

### Metrics Files
```
work/metrics/metrics_001.json
work/metrics/metrics_002.json
work/metrics/metrics_042.json
```

**Pattern:** `metrics_###.json`
- Prefix: `metrics_` (fixed)
- Iteration: `###` (3-digit zero-padded, matches iteration number)
- Extension: `.json`

### Critique Files
```
work/reviews/critique_001.json
work/reviews/critique_002.json
work/reviews/critique_042.json
```

**Pattern:** `critique_###.json`
- Prefix: `critique_` (fixed)
- Iteration: `###` (3-digit zero-padded, matches iteration number)
- Extension: `.json`

### Log Directories
```
work/logs/iter_001/
work/logs/iter_002/
work/logs/iter_042/
```

**Pattern:** `iter_###/`
- Iteration: `iter_###` (3-digit zero-padded)

### Log Files
```
work/logs/iter_001/run.log
work/logs/iter_001/blender_stdout.log
work/logs/iter_001/blender_stderr.log
```

**Pattern:** `{stage}.log`
- Common names: `run.log`, `blender_stdout.log`, `blender_stderr.log`
- Extension: `.log`

## Number Extraction and Formatting

### PowerShell: Extract Latest Version Number
```powershell
# Get latest spec version
$specs = Get-ChildItem -Path "work\spec" -Filter "building_v*.yaml"
$latest = ($specs | ForEach-Object {
    if ($_.Name -match 'building_v(\d+)\.yaml') {
        [int]$matches[1]
    }
} | Measure-Object -Maximum).Maximum

if ($null -eq $latest) { $latest = 0 }
```

### PowerShell: Format Version Number
```powershell
$version = 23
$formatted = "v{0:D3}" -f $version  # Outputs: v023
```

### PowerShell: Extract Latest Iteration Number
```powershell
# Get latest iteration
$iters = Get-ChildItem -Path "work\renders" -Directory -Filter "iter_*"
$latest = ($iters | ForEach-Object {
    if ($_.Name -match 'iter_(\d+)') {
        [int]$matches[1]
    }
} | Measure-Object -Maximum).Maximum

if ($null -eq $latest) { $latest = 0 }
```

### PowerShell: Format Iteration Number
```powershell
$iteration = 42
$formatted = "iter_{0:D3}" -f $iteration  # Outputs: iter_042
```

## Directory Structure Templates

### Iteration Directory Structure
For iteration N (e.g., N=1):
```
work/renders/iter_001/
    front.png
    left.png
    right.png
    rear.png
    iso.png
    top.png
work/metrics/
    metrics_001.json
work/reviews/
    critique_001.json
work/logs/iter_001/
    run.log
exports/glb/
    building_iter_001.glb
```

## Reference Image Naming

Reference images in `inputs/reference/` can have flexible names:
```
inputs/reference/front_view.jpg
inputs/reference/IMG_1234.png
inputs/reference/building_side_01.png
```

**Recommendations:**
- Use descriptive names
- Include view direction if known (front, left, iso, etc.)
- Use common image formats (PNG, JPG, JPEG)

## Notes Naming

Notes files in `inputs/notes/` can have flexible names:
```
inputs/notes/measurements.txt
inputs/notes/assumptions.md
inputs/notes/2025-01-01_observations.txt
```

**Recommendations:**
- Use descriptive names
- Include dates if time-relevant
- Use .txt or .md extensions

## Configuration Naming

```
config/local.env              # Active configuration (gitignored)
config/local.env.example      # Template configuration (committed)
```

## Script Naming

### PowerShell Scripts
```
scripts/run_iteration.ps1     # Main iteration runner
scripts/new_iteration.ps1     # Spec versioning helper
scripts/[purpose].ps1         # Descriptive snake_case or PascalCase
```

### Python Scripts
```
scripts/validate_geometry.py  # Geometry validator
scripts/blender/build_from_spec.py   # Blender builder
scripts/blender/render_views.py      # Blender renderer
scripts/[purpose].py                 # Descriptive snake_case
```

### Prompt Templates
```
scripts/prompts/spec_generator.md    # Spec generation prompt
scripts/prompts/spec_critic.md       # Critique prompt
scripts/prompts/spec_editor.md       # Spec editing prompt
```

## Validation Rules

### Version Number Validation
```powershell
# Valid: v001, v023, v999
# Invalid: v1, v23, v1000 (not 3 digits), 001, 23 (missing 'v')
$version -match '^v\d{3}$'
```

### Iteration Number Validation
```powershell
# Valid: iter_001, iter_042, iter_999
# Invalid: iter_1, iter_42, 001, iter1000
$iteration -match '^iter_\d{3}$'
```

### File Name Validation
```powershell
# Spec file
$specFile -match '^building_v\d{3}\.yaml$'

# GLB file
$glbFile -match '^building_iter_\d{3}\.glb$'

# Metrics file
$metricsFile -match '^metrics_\d{3}\.json$'

# Critique file
$critiqueFile -match '^critique_\d{3}\.json$'
```

## Examples

### Complete Iteration Example

**Setup:**
- Current spec: `work/spec/building_v003.yaml`
- Previous iteration: `iter_007`
- Next iteration: `iter_008`

**Generated Files:**
```
exports/glb/building_iter_008.glb
work/renders/iter_008/front.png
work/renders/iter_008/left.png
work/renders/iter_008/right.png
work/renders/iter_008/rear.png
work/renders/iter_008/iso.png
work/renders/iter_008/top.png
work/metrics/metrics_008.json
work/logs/iter_008/run.log
```

**After Critique:**
```
work/reviews/critique_008.json
```

**After Spec Edit:**
```
work/spec/building_v004.yaml
```

### Version History Example

Timeline showing spec versions and iterations:
```
v001 → iter_001, iter_002 (script fixes)
v002 → iter_003
v003 → iter_004, iter_005, iter_006 (script improvements)
v004 → iter_007
v005 → iter_008 (current)
```
