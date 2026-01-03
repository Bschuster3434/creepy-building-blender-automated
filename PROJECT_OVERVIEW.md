# Autonomous Building Reconstruction System

## Objective

Create an autonomous system that takes a set of reference images of a real-world building and produces a complete, high-quality 3D representation through **four clearly defined phases**.

The system must be repeatable: the same process should work when a new set of reference files is placed into a new folder.

My role is limited to resolving ambiguity and approving phase completion.  
Your role is to determine *how* to achieve each phase outcome.

---

## Phase 1A — Base Structure with Cutouts (GEOMETRY ONLY)

### Outcome

Produce the **base building structure** with **rectangular cutouts** (holes) where windows and doors will be placed.

### What IS Included in Phase 1A

- All structural walls (front, left, right, rear)
- Roof surface
- Foundation
- Parapet with stepping configuration
- Canopy structure and support posts
- Chimney
- **Rectangular cutouts** (Boolean voids/holes) at all door and window locations
- Clean, manifold geometry without artifacts

### What IS NOT Included in Phase 1A

- **NO window frames, glass, or mullions** - only cutouts (holes) in walls
- **NO door panels or frames** - only cutouts (holes) for doors
- **NO materials or textures** - geometry only
- **NO realistic colors** - use simple placeholder colors:
  - Walls: medium gray (#808080)
  - Roof: dark gray (#404040)
  - Cutouts: black (#000000) for high contrast visibility
  - Structural elements: brown/gray to distinguish parts
- **NO environment, ground, or lighting** - building only

### Success Criteria

The base structure must:

- Have all structural elements present with correct dimensions
- Have **rectangular cutouts** (actual holes, not just colored surfaces) at all opening locations
- Cutouts must have correct dimensions and positions per specification
- Be free of visual artifacts (overlapping faces, z-fighting, broken normals)
- Be manifold and geometrically sound
- Export successfully as GLB
- **Load and render correctly in Three.js** (web compatibility verified)

**Cutouts should be visible as voids/holes - you can see through them.**

### Phase 1A Approval Gate

Phase 1A is complete when:
1. All base structure elements built and verified in renders
2. All cutouts present and visible as holes
3. GLB exports successfully
4. **Three.js validation passes** (loads without errors)
5. User explicitly approves: **"Base structure with cutouts is correct, proceed to Phase 1B"**
6. Base geometry is **FROZEN** - no modifications to base structure allowed after this point

**Phase 1A must be approved before Phase 1B begins.**

---

## Phase 1B — Opening Fill (WINDOW & DOOR GEOMETRY)

### Prerequisites

- **Phase 1A base structure APPROVED and FROZEN**
- Base geometry (walls, roof, foundation, etc.) may NOT be modified in Phase 1B

### Outcome

Add **window frames, glass, and door panels** to fill the cutouts created in Phase 1A.

### What IS Included in Phase 1B

- Window frames for all window openings
- Window glass geometry (panes, mullions if applicable)
- Door panels and frames for all door openings
- Door glass (if applicable, e.g., storefront doors)
- All geometry that sits within the Phase 1A cutouts

### What IS NOT Included in Phase 1B

- **NO modifications to Phase 1A base structure** - walls, roof, foundation are frozen
- **NO materials or textures** - still placeholder colors only:
  - Window frames: white (#FFFFFF) for visibility
  - Window glass: black (#000000) as placeholder
  - Door frames: brown (#8B4513)
  - Door panels: very dark gray (#1A1A1A)
- **NO environment, ground, or lighting** - building only

### Success Criteria

The complete geometry must:

- Have all window frames, glass, and doors present and correctly positioned
- Fill all cutouts from Phase 1A appropriately
- Preserve Phase 1A base geometry **exactly** (verification: vertex/face counts must match)
- Be free of visual artifacts
- Be manifold and geometrically sound
- Export successfully as GLB
- **Load and render correctly in Three.js**

**Phase 1A base structure MUST remain completely unchanged.**

### Phase 1B Approval Gate

Phase 1B is complete when:
1. All opening geometry built and verified in renders
2. All cutouts properly filled with frames, glass, doors
3. Phase 1A geometry verified as unchanged (vertex/face count check)
4. GLB exports successfully
5. **Three.js validation passes** (loads without errors)
6. User explicitly approves: **"Complete geometry with openings is correct, proceed to Phase 2"**
7. **ALL geometry is FROZEN** - no further geometry changes allowed

**Phase 1B must be approved before Phase 2 begins.**

---

## Phase 2 — Building Appearance (MATERIALS ONLY)

### Prerequisites

- **Phase 1A and 1B geometry APPROVED and FROZEN**
- ALL geometry may NOT be modified in Phase 2

### Outcome

Produce a **visually complete building** by applying realistic materials and textures to the frozen geometry.

### What IS Included in Phase 2

- All materials (brick, concrete, metal, glass)
- All textures and surface detail
- **Realistic aesthetic** - clean, well-maintained commercial building appearance
- Appropriate weathering for building age (light weathering, not abandoned)
- Surface properties (roughness, metallic, opacity, normal maps)
- Color accuracy for realistic commercial building materials

### What IS NOT Included in Phase 2

- **NO geometry changes** - mesh is frozen from Phase 1A/1B
- **NO abandoned/creepy aesthetic** - building should look functional and maintained
- **NO excessive weathering or decay** - light weathering only
- **NO environment or context** - building only
- **NO lighting setup** - use neutral lighting for material evaluation

### Material Aesthetic Guidelines

**Realistic, Well-Maintained Commercial Building:**
- Brick: Clean red/terracotta with minimal weathering (5-10% color variation)
- Glass: Transparent (85-90%), clear visibility, NOT opaque black
- Window frames: Clean white painted aluminum, minimal rust
- Metal posts: 80-90% paint coverage, light rust at joints only (8% coverage)
- Roof: Standard tar and gravel, medium gray, fair condition
- Foundation: Light gray concrete, minor cracks acceptable
- Overall: Building should look functional, not abandoned

### Success Criteria

The result must:

- Preserve the exact geometry from Phase 1A/1B (verification: vertex/face counts match)
- Apply materials consistently across surfaces
- Produce believable surface detail without altering structure
- Maintain continuity across edges and corners
- Achieve **realistic, well-maintained aesthetic** (NOT creepy/abandoned)
- Have transparent glass windows (NOT opaque black)
- Have clean materials with appropriate minimal weathering for building age
- Export successfully as GLB
- **Load and render correctly in Three.js with materials**

**This phase concerns appearance only. No structural changes are allowed.**

### Phase 2 Approval Gate

Phase 2 is complete when:
1. All materials applied and verified in renders
2. Materials achieve realistic, well-maintained aesthetic
3. Glass is transparent (not opaque)
4. Geometry verified as unchanged from Phase 1B
5. GLB exports successfully with materials
6. **Three.js validation passes** (materials load correctly)
7. User explicitly approves: **"Realistic appearance is correct, proceed to Phase 3"**
8. Building (mesh + materials) is **FROZEN** - no further changes allowed

**Phase 2 must be approved before Phase 3 begins.**

---

## Phase 3 — Environment (SCENE COMPOSITION)

### Prerequisites

- **Phase 1A, 1B, and Phase 2 APPROVED and FROZEN**
- Building may NOT be modified in Phase 3

### Outcome

Produce a **complete scene** by placing the building into a surrounding environment suitable for Three.js web viewing.

### What IS Included in Phase 3

- Ground surface and terrain (asphalt, concrete, or gravel)
- Surrounding context (appropriate vegetation, parking area, etc.)
- Lighting setup optimized for Three.js rendering (time of day, shadows, atmosphere)
- Camera positioning for web viewer (orbit and first-person modes)
- Any environmental effects appropriate for realistic commercial setting

### What IS NOT Included in Phase 3

- **NO building modifications** - geometry and materials are frozen
- **NO abandoned/overgrown aesthetic** - maintain realistic commercial setting
- Focus is entirely on context and presentation

### Success Criteria

The environment must:

- Establish correct scale and orientation
- Include ground, surrounding context, and lighting optimized for web rendering
- Support navigation in Three.js viewer (orbit and first-person walkthrough)
- Treat the building as a finished, immutable object
- Complement the realistic, well-maintained building aesthetic
- Export successfully as GLB (may include environment elements)
- **Load and render correctly in Three.js viewer**

### Phase 3 Approval Gate

Phase 3 is complete when:
1. Environment and scene composition verified in renders
2. Scene works correctly in Three.js viewer (orbit + walkthrough modes)
3. GLB exports successfully with environment
4. **Three.js validation passes** (complete scene loads)
5. User explicitly approves: **"Scene is complete, project finished"**

**This is the final phase.**  

---

## Autonomy Expectations

You are expected to:

- Analyze reference images  
- Infer structure, proportions, and layout  
- Decide what is certain, inferable, or ambiguous  
- Create internal representations or specifications as needed  
- Build, evaluate, revise, and iterate within each phase  

You may:

- Create sub-agents or internal roles  
- Define intermediate steps or artifacts  
- Design validation and review processes  

You must:

- Track uncertainty explicitly  
- Avoid silent assumptions  
- Improve outputs through iteration  

---

## Human Interaction Rules

Only involve me when one of the following occurs:

1. **Ambiguity**  
   - Multiple plausible interpretations exist that materially affect the outcome  

2. **Missing Evidence**  
   - A required aspect of the phase cannot be reasonably inferred  

3. **Phase Approval**  
   - You believe a phase has met its outcome and is ready to be frozen  

When stopping for input:

- Present a short list of decisions  
- Provide a recommended default for each  
- Do not ask for subjective visual feedback  

---

## Success Criteria

This project is successful when:

- I can place reference images into a folder  
- Run the system  
- Answer a small number of clarification questions  
- Receive a finished result for each phase  

Without needing to:

- Inspect meshes manually  
- Debug modeling issues  
- Direct how the work is done  

---

## Starting Instruction

Begin by:

1. Examining the provided reference images
2. Determining what is certain, inferable, or ambiguous
3. Designing and executing whatever internal process is required to achieve **Phase 1A — Base Structure with Cutouts**
4. Proceeding autonomously until a decision or approval is required

## Three.js Web Viewer Requirement

All phases must validate successfully in Three.js:

- GLB exports must load without errors in Three.js
- Geometry must render correctly in web browser
- Materials must display properly in Three.js shader system
- Final deliverable includes working web viewer with:
  - **Orbit controls** (rotate, zoom, pan with mouse)
  - **First-person walkthrough** (WASD movement, mouse look)
  - Phase selector to view different stages
  - Responsive design for browser compatibility

**Three.js validation is required after each phase before user approval.**  
