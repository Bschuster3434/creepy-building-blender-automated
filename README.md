# AI-First Vision → Spec → Blender Pipeline

An iterative, deterministic pipeline for generating and refining 3D building models from reference images using AI-driven specifications and automated Blender geometry generation.

## Pipeline Stages

### Stage 1: Reference Ingestion
- Input: Reference photos/images of the building
- Location: `inputs/reference/`
- Output: Organized reference set for spec generation

### Stage 2: Spec Generation
- Input: Reference images + notes
- Process: AI generates structured YAML specification
- Output: `work/spec/building_v###.yaml`
- Schema: Dimensions, materials, openings, tolerances

### Stage 3: Geometry Generation
- Input: YAML spec
- Process: Headless Blender builds 3D geometry from spec
- Output:
  - `exports/glb/building_iter_###.glb`
  - Standardized renders in `work/renders/iter_###/`
  - Metrics JSON in `work/metrics/metrics_###.json`

### Stage 4: Render Generation
- Process: Fixed camera positions render standardized views
- Views: front, left, right, rear, iso, top
- Output: PNG renders for comparison

### Stage 5: Critique & Analysis
- Input: Reference images + generated renders + metrics
- Process: AI compares renders to references
- Output: `work/reviews/critique_###.json` (structured diff/feedback)

### Stage 6: Spec Update
- Input: Critique JSON + current spec
- Process: AI edits YAML spec based on critique
- Output: `work/spec/building_v###.yaml` (new version)

### Repeat Stages 3-6 until convergence

## Folder Structure

```
├── inputs/
│   ├── reference/       # Reference photos and images
│   └── notes/           # Manual notes and constraints
├── work/
│   ├── spec/            # YAML specifications (building_v001.yaml, etc.)
│   ├── renders/         # Iteration renders (iter_001/, iter_002/, etc.)
│   ├── metrics/         # Geometry metrics (metrics_001.json, etc.)
│   ├── reviews/         # Critique outputs (critique_001.json, etc.)
│   ├── verification/    # Verification checkpoints
│   └── logs/            # Execution logs (iter_001/run.log, etc.)
├── scripts/
│   ├── blender/         # Blender Python scripts
│   ├── prompts/         # AI prompt templates
│   ├── run_iteration.ps1      # Main iteration runner
│   ├── new_iteration.ps1      # Spec versioning helper
│   └── validate_geometry.py   # Geometry validation
├── exports/
│   ├── glb/             # Final GLB exports (building_iter_###.glb)
│   └── renders/         # Final/approved renders
├── docs/
│   ├── CONTRACT.md      # I/O schemas and contracts
│   ├── NAMING.md        # File naming conventions
│   └── AGENT_INSTRUCTIONS.md  # Phase-aware agent behavior
├── viewer/              # Three.js web viewer (React + Vite)
├── .claude/             # Claude Code project instructions
└── config/
    └── local.env        # Local environment config (BLENDER_PATH, etc.)
```

## File Flow Through Pipeline

1. **Reference Images** → `inputs/reference/`
2. **AI Spec Generator** → `work/spec/building_v001.yaml`
3. **Blender Builder** → `exports/glb/building_iter_001.glb` + renders + metrics
4. **AI Critic** → `work/reviews/critique_001.json`
5. **AI Spec Editor** → `work/spec/building_v002.yaml`
6. **Loop back to step 3 with new spec**

## Naming Conventions

### Version Numbers (Specs)
- Format: `building_v###.yaml` (e.g., `building_v001.yaml`, `building_v023.yaml`)
- Increments when spec is manually or AI-edited
- Zero-padded to 3 digits

### Iteration Numbers (Builds)
- Format: `iter_###` (e.g., `iter_001`, `iter_042`)
- Increments each time geometry is built from a spec
- Zero-padded to 3 digits
- One spec version may produce multiple iterations (e.g., different Blender script versions)

### File Naming Examples
```
work/spec/building_v001.yaml
work/spec/building_v002.yaml
exports/glb/building_iter_001.glb
exports/glb/building_iter_002.glb
work/renders/iter_001/front.png
work/renders/iter_001/iso.png
work/metrics/metrics_001.json
work/reviews/critique_001.json
work/logs/iter_001/run.log
```

## Getting Started

### 1. Configure Environment
```powershell
# Copy example config
cp config\local.env.example config\local.env

# Edit config\local.env and set BLENDER_PATH
# Example: BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.0\blender.exe
```

### 2. Add Reference Images
```powershell
# Place reference photos in inputs/reference/
# Add any notes to inputs/notes/
```

### 3. Create Initial Spec
```powershell
# Manually create or AI-generate work/spec/building_v001.yaml
# Use existing spec_2.yaml as starting point if needed
```

### 4. Run First Iteration
```powershell
.\scripts\run_iteration.ps1
```

### 5. Review Outputs
- Check renders in `work/renders/iter_001/`
- Review metrics in `work/metrics/metrics_001.json`
- Examine logs in `work/logs/iter_001/run.log`

### 6. Iterate
```powershell
# Generate critique (manual or AI)
# Update spec to building_v002.yaml (use new_iteration.ps1)
# Run next iteration
.\scripts\run_iteration.ps1
```

## Scripts

### `run_iteration.ps1`
Main pipeline runner. Executes one full iteration:
- Finds latest spec version
- Determines next iteration number
- Runs Blender headless to build geometry
- Generates renders and metrics
- Logs all output

### `new_iteration.ps1`
Spec versioning helper. Creates new spec version:
- Copies latest `building_v###.yaml` to `v###++`
- Adds timestamp and change message
- Preserves git history

### `validate_geometry.py`
Geometry quality checker. Validates:
- Non-manifold geometry
- Mesh intersections
- Coplanar faces
- Dimension tolerances

## Requirements

- **Blender** (configured in `config/local.env`)
- **Python 3.8+** (for standalone validation scripts)
- **PowerShell 5.1+** (Windows)

## Status

**Project Complete.** All three phases have been successfully executed:

- **Phase 1**: Geometry (1A: base structure, 1B: windows/doors, 1C: interior) ✓
- **Phase 2**: Building appearance (materials and textures) ✓
- **Phase 3**: Environment (road, parking lot, lighting) ✓

The final model is available in `exports/glb/` and can be viewed in the Three.js web viewer (`viewer/`).
