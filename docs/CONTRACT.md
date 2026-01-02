# Pipeline Contracts

This document defines the input/output schemas and contracts between pipeline stages.

## File Schemas

### Building Specification YAML

**Location:** `work/spec/building_v###.yaml`

**Required Fields:**

```yaml
version: string              # Format: v001, v002, etc.
units: string                # "meters" | "feet" | "centimeters"

assumptions: list[string]    # List of assumptions made

overall:
  footprint:
    shape: string            # "rectangle" | "polygon" | "L-shape" etc.
    width: float             # X-dimension
    depth: float             # Y-dimension
  height:
    wall_height: float       # Height to roof/parapet base
    parapet_height: float    # Additional parapet height (0 if none)
    total_height: float      # wall_height + parapet_height

walls:
  thickness: float           # Wall thickness
  material: string           # Material identifier
  height: float              # Same as overall.height.wall_height

roof:
  type: string               # "flat" | "gabled" | "hipped" | "shed"
  thickness: float           # Roof slab thickness
  elevation: float           # Bottom of roof elevation

openings:
  doors: list[Door]          # List of door specifications
  windows: list[Window]      # List of window specifications

materials:
  walls: string              # Material for walls
  roof: string               # Material for roof
  door: string               # Material for doors
  windows: string            # Material for windows

tolerances:
  dimension_tolerance: float      # Acceptable dimension error (meters)
  angle_tolerance_degrees: float  # Acceptable angle error (degrees)
  allow_non_manifold: bool        # Whether non-manifold geometry is acceptable

coordinate_system:
  origin: string             # "center_of_footprint_at_ground" etc.
  axes:
    x: string                # "left_right"
    y: string                # "front_back"
    z: string                # "up"
```

**Door Schema:**
```yaml
- id: string                 # Unique identifier
  type: string               # "single" | "double"
  width: float               # Door width
  height: float              # Door height
  wall: string               # "front" | "left" | "right" | "rear"
  position:
    x: float                 # X-offset from center
    sill_height: float       # Height above ground (usually 0 for doors)
```

**Window Schema:**
```yaml
- id: string                 # Unique identifier
  width: float               # Window width
  height: float              # Window height
  wall: string               # "front" | "left" | "right" | "rear"
  position:
    x: float                 # X-offset from center
    sill_height: float       # Height above ground
```

### Geometry Metrics JSON

**Location:** `work/metrics/metrics_###.json`

**Schema:**

```json
{
  "status": "success|error|stub",
  "iteration": 1,
  "spec_version": "v001",
  "timestamp": "2025-01-01T12:00:00Z",
  "vertex_count": 1234,
  "face_count": 567,
  "edge_count": 890,
  "non_manifold_edges": 0,
  "intersecting_faces": 0,
  "dimension_checks": [
    {
      "element": "overall_width",
      "expected": 9.5,
      "actual": 9.502,
      "error": 0.002,
      "within_tolerance": true
    }
  ],
  "dimension_errors": [],
  "warnings": []
}
```

### Critique JSON

**Location:** `work/reviews/critique_###.json`

**Schema:**

```json
{
  "iteration": 1,
  "spec_version": "v001",
  "timestamp": "2025-01-01T12:00:00Z",
  "overall_assessment": {
    "status": "needs_improvement|acceptable|excellent",
    "summary": "Brief overall assessment",
    "convergence_estimate": "30%"
  },
  "geometric_issues": [
    {
      "severity": "critical|major|minor",
      "category": "dimension|proportion|alignment|material|missing_element",
      "element": "element identifier",
      "description": "Clear description",
      "evidence": {
        "view": "front|left|right|rear|iso|top",
        "reference_observation": "What you see in reference",
        "render_observation": "What you see in render"
      },
      "suggested_fix": {
        "spec_path": "dotted.path.to.field",
        "current_value": "current value",
        "suggested_value": "suggested value",
        "reasoning": "Why this change"
      }
    }
  ],
  "material_issues": [
    {
      "severity": "major|minor",
      "element": "element identifier",
      "description": "Material appearance issue",
      "suggested_fix": {
        "spec_path": "materials.walls",
        "current_value": "current_material",
        "suggested_value": "suggested_material",
        "reasoning": "Explanation"
      }
    }
  ],
  "metrics_review": {
    "non_manifold_edges": 0,
    "intersecting_faces": 0,
    "issues": []
  },
  "positive_aspects": [],
  "next_priorities": []
}
```

## Pipeline Stage Contracts

### Stage: Spec Generation

**Input:**
- Reference images: `inputs/reference/*.{png,jpg}`
- Optional notes: `inputs/notes/*.txt`
- Optional previous spec: `work/spec/building_v###.yaml`

**Output:**
- YAML spec: `work/spec/building_v###.yaml`

**Contract:**
- Output YAML must be valid and parse without errors
- All required fields must be present
- All dimensions must be positive numbers
- Openings must reference valid walls ("front", "left", "right", "rear")
- Materials must be consistent (no dangling references)

### Stage: Geometry Generation

**Input:**
- YAML spec: `work/spec/building_v###.yaml`

**Output:**
- GLB export: `exports/glb/building_iter_###.glb`
- Renders: `work/renders/iter_###/{front,left,right,rear,iso,top}.png`
- Metrics JSON: `work/metrics/metrics_###.json`

**Contract:**
- GLB must be valid GLB 2.0 format
- All 6 renders must be generated (PNG format, same resolution)
- Metrics JSON must be valid JSON matching schema
- If build fails, metrics JSON must still be written with status="error"

### Stage: Critique Generation

**Input:**
- Reference images: `inputs/reference/*.{png,jpg}`
- Renders: `work/renders/iter_###/*.png`
- Current spec: `work/spec/building_v###.yaml`
- Metrics: `work/metrics/metrics_###.json`

**Output:**
- Critique JSON: `work/reviews/critique_###.json`

**Contract:**
- Output JSON must be valid and match schema
- All issues must include severity, description, evidence
- Suggested fixes must include spec_path, current_value, suggested_value
- overall_assessment must include convergence_estimate

### Stage: Spec Editing

**Input:**
- Current spec: `work/spec/building_v###.yaml`
- Critique JSON: `work/reviews/critique_###.json`

**Output:**
- Updated spec: `work/spec/building_v###++.yaml`

**Contract:**
- Output YAML must be valid
- Version number must increment
- Header comment must document changes
- All suggested fixes from "critical" issues must be applied
- Schema compliance maintained

## Iteration Flow Contract

**Sequential Order:**
1. Spec exists (manually created or from previous iteration)
2. Geometry generation runs → produces GLB + renders + metrics
3. Critique runs → produces critique JSON
4. Spec editing runs → produces new spec version
5. Loop back to step 2

**Invariants:**
- Iteration numbers always increment
- Spec version numbers always increment when spec changes
- One spec version may have multiple iterations (script improvements)
- Renders, metrics, and critiques use iteration numbers
- Specs use version numbers

## Error Handling Contract

**All scripts must:**
- Exit with code 0 on success
- Exit with non-zero code on failure
- Write error messages to stderr
- Write progress messages to stdout
- Handle missing files gracefully with clear error messages
- Validate inputs before processing
- Create output directories if they don't exist
