# Agent Instructions - Phase-Aware Behavior

This document defines how each agent should behave in each phase of the building reconstruction pipeline.

**Phase State:** Tracked in `work/phase_state.json`
**Phase Specs:** Each phase has its own spec file:
- Phase 1A: `work/spec/phase_1a/building_geometry.yaml`
- Phase 1B: `work/spec/phase_1b/building_geometry_openings.yaml` (created after 1A approval)
- Phase 2: `work/spec/phase_2/building_materials.yaml` (created after 1B approval)
- Phase 3: `work/spec/phase_3/building_environment.yaml` (created after Phase 2 approval)

---

## Phase 1A: Base Structure with Cutouts (GEOMETRY ONLY)

**Spec File:** `work/spec/phase_1a/building_geometry.yaml`

### Blender Operator Agent - Phase 1A Mode

#### Scope
Build base structure with RECTANGULAR CUTOUTS (Boolean holes) for openings. PLACEHOLDER COLORS only.

#### What to Build
- All structural elements (walls, roof, parapet, chimney, foundation)
- Canopy structure and support posts
- **Rectangular cutouts** (Boolean voids/holes) at all door and window locations
- Clean, manifold geometry without artifacts

#### What NOT to Build (Phase 1B)
- ❌ NO window frames, glass, or mullions yet
- ❌ NO door panels or frames yet
- ❌ Only cutouts (holes), not the actual window/door objects

#### Materials - PLACEHOLDER COLORS ONLY
```yaml
walls: "#808080" (medium gray)
roof: "#404040" (dark gray)
parapet: "#8B4513" (brown - to distinguish from walls)
canopy_roof: "#C0C0C0" (light gray)
canopy_posts: "#8B4513" (brown)
foundation: "#606060" (dark gray)
chimney: "#8B4513" (brown)
cutouts: "#000000" (black - to make holes visible)
```

#### Cutout Requirements (CRITICAL)
- Cutouts must be actual HOLES (Boolean difference operations), not just black rectangles
- User should be able to see through the cutouts
- Cutout dimensions and positions must match spec exactly
- Verify cutouts exist by looking through them in viewport

#### What NOT to Do
- ❌ DO NOT create window/door geometry (that's Phase 1B)
- ❌ DO NOT apply realistic colors
- ❌ DO NOT apply textures
- ❌ DO NOT add weathering or surface detail
- ❌ DO NOT use image textures
- ❌ DO NOT add bump/normal maps

#### Verification Requirements
- After building each major element, capture a viewport screenshot
- **Verify cutouts are visible as HOLES** (can see through them)
- Verify all structural elements from spec are present
- Count objects created and compare to expected
- Test GLB export before completing

#### Output
- GLB export: `exports/glb/building_phase_1a_iter_###.glb`
- Renders: `work/renders/phase_1a_iter_###/*.png` (6 standard views)
- Metrics: `work/metrics/phase_1a_metrics_###.json`
- Build log documenting what was created
- **Three.js validation** must pass before phase approval

---

### Visual Critic Agent - Phase 1A Mode

#### Scope
Critique BASE STRUCTURE and CUTOUTS ONLY. Ignore missing windows/doors (they're for Phase 1B).

#### What to Critique

**CRITICAL ISSUES (Block progress):**
- Missing structural elements (walls, roof, parapet, chimney, foundation)
- **Missing cutouts** (no holes where windows/doors should be)
- **Cutouts are not actual holes** (just black colored rectangles instead of voids)
- Incorrect dimensions (>10% error from spec)
- Incorrect cutout positions
- Incorrect footprint shape
- Geometry artifacts (non-manifold, z-fighting, overlapping faces)

**MAJOR ISSUES (Should fix):**
- Cutout dimensions slightly off (5-10% error)
- Cutout positioning errors
- Proportions slightly off (5-10% error from spec)
- Element counts wrong (wrong number of posts, etc.)

**MINOR ISSUES (Nice to fix):**
- Small dimensional refinements (<5% error)
- Subtle proportion adjustments

#### What NOT to Critique

**IGNORE these in Phase 1A (they're for Phase 1B or later):**
- ❌ Missing window frames ("where are the frames?") → Phase 1B
- ❌ Missing door panels ("no doors visible") → Phase 1B
- ❌ Missing glass ("windows should have glass") → Phase 1B
- ❌ Colors being wrong ("brick should be red not gray") → Phase 2
- ❌ Missing textures ("no brick pattern visible") → Phase 2
- ❌ Missing weathering ("no rust on posts") → Phase 2
- ❌ Material properties ("should be more metallic") → Phase 2

#### Special Rule for Phase 1A
- **Cutouts (holes) should be present** - this IS a Phase 1A requirement
- **Window/door objects should NOT be present** - this is Phase 1B, not a Phase 1A issue
- ONLY flag material/color issues if they **prevent geometry evaluation**

#### Output Format
```json
{
  "phase": "1a",
  "mode": "base_structure_with_cutouts",
  "geometric_issues": [...],
  "cutout_issues": [...],  // Missing or incorrectly positioned holes
  "material_issues": [],  // Empty or only rendering visibility issues
  "phase_1a_convergence": "X%",
  "phase_1a_recommendation": "iterate | approve"
}
```

---

### Spec Architect Agent - Phase 1 Mode

#### Scope
Generate specs focused on GEOMETRY with minimal material section.

#### Required Sections (Full Detail)
- version
- units
- assumptions
- overall (footprint, dimensions)
- walls (dimensions, NOT detailed materials)
- roof (geometry, NOT detailed materials)
- parapet (geometry, stepping configuration)
- openings (all doors/windows with exact dimensions and positions)
- canopy (geometry, posts)
- chimney (position, dimensions)
- foundation (geometry)
- coordinate_system
- tolerances

#### Material Section (MINIMAL)
```yaml
materials:
  placeholder_colors:
    walls: "#808080"
    roof: "#404040"
    parapet: "#8B4513"
    canopy_roof: "#C0C0C0"
    canopy_posts: "#8B4513"
    foundation: "#606060"
    chimney: "#8B4513"
    windows: "#000000"
    doors: "#1A1A1A"

  # DO NOT include material_details section in Phase 1
  # That's for Phase 2
```

#### What NOT to Include
- ❌ Detailed material_details section
- ❌ Texture specifications
- ❌ Weathering patterns
- ❌ Surface properties (roughness, metallic, etc.)

---

### Quality Gatekeeper Agent - Phase 1 Mode

#### Scope
Validate spec for GEOMETRY completeness.

#### What to Validate

**REQUIRED in Phase 1:**
- All geometry sections present and complete
- All dimensions are positive numbers
- All positions are within building bounds
- All openings reference valid walls
- Coordinate system is defined
- Placeholder colors are defined

**NOT REQUIRED in Phase 1:**
- ❌ Detailed material_details section (Phase 2)
- ❌ Texture specifications (Phase 2)
- ❌ Weathering patterns (Phase 2)

#### Validation Logic
```python
if phase == 1:
    require(geometry_sections_complete)
    require(placeholder_colors_defined)
    allow(material_details_missing)  # OK for Phase 1
else if phase == 2:
    require(geometry_frozen)
    require(material_details_complete)
```

---

### Iteration Orchestrator Agent - Phase 1 Mode

#### Scope
Decide when Phase 1 is complete and ready for user approval.

#### Phase 1 Completion Criteria

**Geometry must meet ALL:**
1. Convergence ≥ 85% for geometric accuracy
2. Zero CRITICAL geometric issues
3. All structural elements present
4. All openings present and positioned correctly
5. Dimensions within tolerance

**When to Recommend Approval:**
```python
if (
    geometric_convergence >= 85% and
    critical_geometric_issues == 0 and
    major_geometric_issues <= 2
):
    recommend("Phase 1 ready for user approval")
else:
    recommend("Continue iteration in Phase 1")
```

#### Phase Gate Enforcement

**MUST get user approval before Phase 2:**
```
Status: "Phase 1 appears complete (85% convergence, 0 critical issues)"
Action Required: Ask user: "Approve Phase 1 mesh and proceed to Phase 2?"
Options:
  1. Approve → Update phase_state.json, freeze geometry, proceed to Phase 2
  2. Iterate more → Continue Phase 1 refinements
  3. Reject → Identify issues and rebuild
```

**DO NOT automatically proceed to Phase 1B** even if criteria are met.

---

## Phase 1B: Opening Fill (WINDOW & DOOR GEOMETRY)

**Spec File:** `work/spec/phase_1b/building_geometry_openings.yaml` (created after Phase 1A approval)

### Blender Operator Agent - Phase 1B Mode

#### Scope
Add window frames, glass, and door panels to FROZEN base structure. PLACEHOLDER COLORS only.

#### Prerequisites
- Phase 1A approved and base geometry FROZEN
- Base structure (walls, roof, foundation, etc.) may NOT be modified

#### What to Build
- Window frames for all window cutouts
- Window glass geometry (panes, mullions if applicable)
- Door panels and frames for all door cutouts
- Door glass (if applicable, e.g., storefront glass doors)
- All geometry that fills the cutouts from Phase 1A

#### What NOT to Build
- ❌ DO NOT modify Phase 1A base geometry (walls, roof, foundation, parapet, canopy, chimney)
- ❌ DO NOT change cutout dimensions or positions
- ❌ DO NOT add or remove structural elements

#### Materials - PLACEHOLDER COLORS ONLY
```yaml
# Carry forward Phase 1A colors, plus:
window_frames: "#FFFFFF" (white - for visibility against gray walls)
window_glass: "#000000" (black - placeholder, will be transparent in Phase 2)
door_frames: "#8B4513" (brown)
door_panels: "#1A1A1A" (very dark gray)
```

#### Geometry Freeze Verification (CRITICAL)
- **Before making ANY changes:** Record baseline vertex count and face count from Phase 1A GLB
- **After adding openings:** Verify base geometry vertex/face counts match exactly
- If counts differ → ERROR, base geometry was modified (not allowed)
- Only opening geometry should add new vertices/faces

#### What NOT to Do
- ❌ DO NOT modify base structure
- ❌ DO NOT apply realistic colors or materials
- ❌ DO NOT apply textures
- ❌ DO NOT add weathering
- ❌ DO NOT make glass transparent yet (Phase 2)

#### Verification Requirements
- Verify Phase 1A base geometry unchanged (vertex/face count check)
- Verify all cutouts now have window/door geometry filling them
- Capture viewport screenshots showing filled openings
- Test GLB export before completing

#### Output
- GLB export: `exports/glb/building_phase_1b_iter_###.glb`
- Renders: `work/renders/phase_1b_iter_###/*.png` (6 standard views)
- Metrics: `work/metrics/phase_1b_metrics_###.json` (include geometry freeze verification)
- Build log documenting openings added and freeze verification results
- **Three.js validation** must pass before phase approval

---

### Visual Critic Agent - Phase 1B Mode

#### Scope
Critique OPENING GEOMETRY ONLY. Assume base structure is correct and frozen.

#### What to Critique

**CRITICAL ISSUES (Block progress):**
- **Base geometry was modified** (vertex/face counts changed from Phase 1A)
- Missing window frames
- Missing door panels
- Cutouts not filled (still empty holes)
- Window/door dimensions incorrect
- Window/door positioning incorrect

**MAJOR ISSUES (Should fix):**
- Frame proportions slightly off (5-10% error)
- Glass geometry missing or incorrectly sized
- Door/window details incomplete

**MINOR ISSUES (Nice to fix):**
- Small dimensional refinements (<5% error)
- Aesthetic improvements to frames/panels

#### What NOT to Critique

**IGNORE these in Phase 1B:**
- ❌ Base structure issues (walls, roof, etc.) → Those were approved in Phase 1A, frozen
- ❌ Colors being wrong ("frames should be painted white not placeholder white") → Phase 2
- ❌ Missing textures ("glass should be transparent") → Phase 2
- ❌ Material properties ("glass should be reflective") → Phase 2

#### Special Rule for Phase 1B
- If you notice base structure issues, NOTE them but **do not include in critique**
- Base geometry is frozen - any issues there require rolling back to Phase 1A
- Focus ONLY on opening geometry (frames, glass, doors)

#### Output Format
```json
{
  "phase": "1b",
  "mode": "opening_fill",
  "geometric_issues": [],  // Base geometry frozen
  "opening_issues": [...],  // Window/door geometry issues
  "geometry_freeze_verified": true,  // Base unchanged from Phase 1A
  "material_issues": [],  // Empty or only visibility issues
  "phase_1b_convergence": "X%",
  "phase_1b_recommendation": "iterate | approve"
}
```

---

### Spec Architect Agent - Phase 1B Mode

#### Scope
Add opening element specifications to Phase 1A spec. Base geometry sections UNCHANGED.

#### Required Sections (Add to Phase 1A spec)
```yaml
phase_1b_openings:
  window_frames:
    material: aluminum_painted  # Not actual material, just reference
    thickness: 0.05  # Frame thickness in meters
    color_placeholder: "#FFFFFF"

  window_glass:
    thickness: 0.006  # Standard window glass thickness
    color_placeholder: "#000000"  # Black placeholder (will be transparent in Phase 2)

  door_panels:
    material: metal_or_glass  # Reference only
    thickness: 0.04
    color_placeholder: "#1A1A1A"

  door_frames:
    thickness: 0.06
    color_placeholder: "#8B4513"
```

#### What NOT to Change
- ❌ DO NOT modify Phase 1A geometry sections (walls, roof, foundation, parapet, canopy, chimney, cutouts)
- ❌ DO NOT change dimensions from Phase 1A
- ❌ DO NOT alter cutout positions

#### Validation
- Compare all Phase 1A geometry sections to Phase 1A approved spec
- If ANY Phase 1A geometry field changed → ERROR, reject spec

---

### Quality Gatekeeper Agent - Phase 1B Mode

#### Scope
Validate that opening specs are complete AND Phase 1A geometry is unchanged.

#### What to Validate

**REQUIRED in Phase 1B:**
- All opening element specifications present (window frames, glass, doors)
- Opening dimensions match cutout dimensions from Phase 1A
- Placeholder colors defined for new elements
- **Phase 1A geometry sections completely unchanged**

**Validation Logic:**
```python
if phase == "1b":
    # Verify Phase 1A sections unchanged
    compare(spec_1b.walls, approved_spec_1a.walls)
    compare(spec_1b.roof, approved_spec_1a.roof)
    compare(spec_1b.foundation, approved_spec_1a.foundation)
    # etc. for all Phase 1A sections

    if any_phase_1a_section_changed:
        reject("Phase 1A geometry cannot be modified in Phase 1B")

    # Verify Phase 1B opening specs present
    require(window_frames_spec_complete)
    require(window_glass_spec_complete)
    require(door_specs_complete)
```

---

### Iteration Orchestrator Agent - Phase 1B Mode

#### Scope
Decide when Phase 1B is complete and ready for user approval.

#### Phase 1B Completion Criteria

**Opening geometry must meet ALL:**
1. Convergence ≥ 85% for opening accuracy
2. Zero CRITICAL opening issues
3. All window frames present and correctly sized
4. All door panels present and correctly positioned
5. **Phase 1A base geometry verified as unchanged**

**When to Recommend Approval:**
```python
if (
    opening_convergence >= 85% and
    critical_opening_issues == 0 and
    major_opening_issues <= 2 and
    geometry_freeze_verified == True
):
    recommend("Phase 1B ready for user approval")
else:
    recommend("Continue iteration in Phase 1B")
```

#### Phase Gate Enforcement

**MUST get user approval before Phase 2:**
```
Status: "Phase 1B appears complete (85% convergence, 0 critical issues, base geometry frozen)"
Action Required: Ask user: "Approve Phase 1B openings and proceed to Phase 2?"
Options:
  1. Approve → Update phase_state.json, freeze ALL geometry, proceed to Phase 2
  2. Iterate more → Continue Phase 1B refinements
  3. Reject → Identify issues and rebuild
```

**DO NOT automatically proceed to Phase 2** even if criteria are met.

---

## Phase 2: Building Appearance (MATERIALS ONLY)

**Spec File:** `work/spec/phase_2/building_materials.yaml` (created after Phase 1B approval)

### Blender Operator Agent - Phase 2 Mode

#### Scope
Apply realistic materials and textures to FROZEN geometry.

#### Prerequisites
- Phase 1A and 1B approved and ALL geometry frozen
- Geometry MUST NOT be modified

#### What to Do
- Load Phase 1B approved GLB
- Apply all materials from spec material_details section
- Apply **realistic, well-maintained aesthetic** materials:
  - Clean brick with minimal weathering (5-10% color variation)
  - **Transparent glass** (85-90% transparency, NOT opaque black)
  - Clean painted window frames (white)
  - Painted metal posts with light rust (8% coverage at joints only)
  - Standard commercial roof materials
- Apply surface properties (roughness, metallic, opacity, normal maps)
- Set up proper PBR material nodes in Blender
- Ensure glass transparency is correctly configured

#### What NOT to Do
- ❌ DO NOT modify geometry
- ❌ DO NOT move vertices
- ❌ DO NOT add/remove elements
- ❌ DO NOT change dimensions
- ❌ DO NOT alter mesh structure
- ❌ DO NOT apply creepy/abandoned aesthetic
- ❌ DO NOT make glass opaque/pitch black
- ❌ DO NOT add excessive weathering or decay

#### Verification
- Before: Count vertices/faces from Phase 1B GLB
- After: Verify counts match exactly
- If geometry changed → ERROR, abort
- Verify glass materials are transparent (not opaque)
- Verify aesthetic is realistic (not creepy/abandoned)

#### Output
- Updated GLB: `exports/glb/building_phase_2_iter_###.glb`
- Textured renders: `work/renders/phase_2_iter_###/*.png`
- Material metrics: `work/metrics/phase_2_metrics_###.json`
- **Three.js validation** must pass before phase approval

---

### Visual Critic Agent - Phase 2 Mode

#### Scope
Critique MATERIALS/TEXTURES ONLY for **realistic, well-maintained** aesthetic. Assume geometry is correct.

#### What to Critique

**CRITICAL ISSUES:**
- Materials completely wrong (glass instead of brick)
- Colors drastically wrong (white brick instead of red)
- **Glass is opaque/pitch black** (should be transparent 85-90%)
- **Creepy/abandoned aesthetic applied** (should be realistic/well-maintained)
- Excessive weathering/decay (building looks abandoned instead of functional)

**MAJOR ISSUES:**
- Colors slightly wrong (wrong shade of red brick)
- Textures not realistic enough
- Weathering too heavy (>15% rust coverage on posts)
- Glass transparency incorrect (should be 85-90%, not 100% or 0%)
- Surface properties wrong (too shiny, too matte)
- Window frames not clean white

**MINOR ISSUES:**
- Fine-tuning color accuracy
- Subtle weathering adjustments (keep minimal)
- Detail refinements
- Minor texture improvements

#### What NOT to Critique

**IGNORE these in Phase 2:**
- ❌ Geometry problems ("window is wrong size") → Frozen from Phase 1B
- ❌ Position problems ("door is in wrong place") → Frozen from Phase 1B
- ❌ Dimensional errors ("building is too tall") → Frozen from Phase 1B
- ❌ Missing/incorrect openings → Frozen from Phase 1B

If you notice geometry issues → Note them but **do not include in critique**. Geometry is frozen.

#### Realistic Aesthetic Validation Checklist

When evaluating materials, verify:
- ✓ Brick: Clean red/terracotta with 5-10% color variation (NOT diseased/rotting)
- ✓ Glass: 85-90% transparent (NOT pitch black/opaque)
- ✓ Window frames: Clean white (NOT heavily weathered)
- ✓ Metal posts: 80-90% paint coverage, 8% rust at joints only (NOT 90%+ rust)
- ✓ Roof: Standard gray tar & gravel (NOT severely deteriorated)
- ✓ Overall: Functional, well-maintained appearance (NOT abandoned/creepy)

#### Output Format
```json
{
  "phase": "2",
  "mode": "materials_realistic_aesthetic",
  "geometric_issues": [],  // Empty - geometry is frozen
  "material_issues": [...],
  "aesthetic_compliance": {
    "realistic_not_creepy": true/false,
    "glass_transparency": "X%",
    "weathering_level": "minimal|moderate|excessive",
    "overall_assessment": "well_maintained|aged|abandoned"
  },
  "phase_2_convergence": "X%",
  "phase_2_recommendation": "iterate | approve"
}
```

---

### Spec Architect Agent - Phase 2 Mode

#### Scope
Generate material specifications for FROZEN geometry.

#### Required Sections
- All Phase 1 geometry sections (UNCHANGED, reference only)
- Expanded material_details section with:
  - Exact colors (RGB values or hex codes)
  - Texture types (brick pattern, concrete, rust)
  - Weathering specifications (discoloration, staining, decay)
  - Surface properties (roughness, metallic, opacity)
  - UV mapping notes if needed

#### What NOT to Change
- ❌ DO NOT modify geometry sections
- ❌ DO NOT change dimensions
- ❌ DO NOT alter positions

#### Validation
- Compare geometry sections to Phase 1 approved spec
- If any geometry field changed → ERROR, reject

---

## Phase 3: Environment (SCENE COMPOSITION)

### Blender Operator Agent - Phase 3 Mode

#### Scope
Add environment and context to FROZEN building.

#### Prerequisites
- Phase 1 and 2 approved and frozen
- Building MUST NOT be modified

#### What to Do
- Load Phase 2 approved building
- Add ground surface
- Add vegetation/debris
- Set up lighting (time of day, shadows)
- Position cameras for presentation
- Add atmospheric effects if needed

#### What NOT to Do
- ❌ DO NOT modify building geometry
- ❌ DO NOT modify building materials
- ❌ DO NOT change building in any way

#### Output
- Final scene: `exports/final/scene_complete.blend`
- Final renders: `exports/final/renders/*.png`

---

## Agent Spawn Guidelines

### How to Spawn Phase-Aware Agents

```python
# Read current phase
phase_state = read_json("work/phase_state.json")
current_phase = phase_state["current_phase"]

# Spawn with phase context
Task(
  subagent_type="general-purpose",
  prompt=f"""
  You are the [Agent Name].

  CURRENT PHASE: {current_phase}
  MODE: {get_mode_for_phase(current_phase)}

  Read your phase-specific instructions from:
  docs/AGENT_INSTRUCTIONS.md

  Follow the Phase {current_phase} behavior defined there.

  [Task-specific instructions...]
  """
)
```

### Required Reading for All Agents

Every agent MUST read:
1. `work/phase_state.json` - Know which phase we're in
2. `docs/AGENT_INSTRUCTIONS.md` - Know how to behave in that phase
3. `PROJECT_OVERVIEW.md` - Understand the overall goals

---

## Phase Transition Protocol

### When Phase 1 Completes

1. **Iteration Orchestrator** determines Phase 1 criteria met
2. **Decision Architect** structures approval request for user
3. **User approves** "Mesh is correct, proceed to Phase 2"
4. **Update** `work/phase_state.json`:
   ```json
   {
     "current_phase": 2,
     "phase_1_status": { "approved": true }
   }
   ```
5. **Freeze** Phase 1 geometry (document approved iteration number)
6. **Proceed** with Phase 2 agents

### Rollback Protocol

If user rejects Phase completion:
```json
{
  "current_phase": 1,
  "phase_1_status": {
    "approved": false,
    "rejection_reason": "Windows still not positioned correctly",
    "action": "Continue iteration in Phase 1"
  }
}
```

---

## Summary

| Agent | Phase 1 | Phase 2 | Phase 3 |
|-------|---------|---------|---------|
| **Blender Operator** | Geometry + placeholders | Materials only | Environment only |
| **Visual Critic** | Geometry critique | Material critique | Scene critique |
| **Spec Architect** | Geometry spec | Material spec | Environment spec |
| **Quality Gatekeeper** | Validate geometry | Validate materials | Validate scene |
| **Iteration Orchestrator** | Phase 1 gate | Phase 2 gate | Phase 3 gate |
| **Reference Analyst** | Same in all phases | Same in all phases | Same in all phases |

**Key Principle:** Each phase builds on the previous, but cannot modify what was approved before.
