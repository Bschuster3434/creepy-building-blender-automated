# Autonomous Building Reconstruction System

## Objective

Create an autonomous system that takes a set of reference images of a real-world building and produces a complete, high-quality 3D representation through **three clearly defined phases**.

The system must be repeatable: the same process should work when a new set of reference files is placed into a new folder.

My role is limited to resolving ambiguity and approving phase completion.  
Your role is to determine *how* to achieve each phase outcome.

---

## Phase 1 — Building Mesh (GEOMETRY ONLY)

### Outcome

Produce a **complete and correct 3D building mesh** that represents the real-world structure shown in the reference images.

### What IS Included in Phase 1

- All geometric elements (walls, roof, parapet, chimney, foundation)
- All openings (doors, windows) with correct dimensions and positions
- All structural features (canopy, posts, steps, recesses)
- Clean, manifold geometry without artifacts

### What IS NOT Included in Phase 1

- **NO materials or textures** - geometry only
- **NO weathering or surface detail** - shapes only
- **NO realistic colors** - use simple placeholder colors for visibility:
  - Walls: neutral gray or simple solid color
  - Openings: contrasting color to verify they exist
  - Structural elements: basic colors to distinguish parts
- **NO environment, ground, or lighting** - building only

### Success Criteria

The mesh must:

- Accurately reflect the building's proportions, layout, and major structural features
- Be free of visual artifacts (e.g., overlapping faces, z-fighting, broken normals)
- Be internally consistent and geometrically sound
- Be organized in a way that supports coherent surface continuity
- Be regenerable from a single authoritative representation (spec or equivalent)
- Have ALL openings (doors, windows) present and verifiable in renders

**At the end of this phase, the building must be structurally correct, even if it has no visual detail.**

### Phase 1 Approval Gate

Phase 1 is complete when:
1. All geometry is built and verified in renders
2. User explicitly approves: **"Mesh is correct, proceed to Phase 2"**
3. Mesh is **FROZEN** - no further geometry changes allowed

**Phase 1 must be approved before Phase 2 begins.**

---

## Phase 2 — Building Appearance (MATERIALS ONLY)

### Prerequisites

- **Phase 1 mesh APPROVED and FROZEN**
- Geometry may NOT be modified in Phase 2

### Outcome

Produce a **visually complete building** by applying materials and textures to the Phase 1 mesh.

### What IS Included in Phase 2

- All materials (brick, concrete, metal, glass)
- All textures and surface detail
- All weathering patterns (rust, discoloration, decay)
- All color accuracy matching reference images
- Surface properties (roughness, metallic, opacity)

### What IS NOT Included in Phase 2

- **NO geometry changes** - mesh is frozen from Phase 1
- **NO environment or context** - building only
- **NO lighting setup** - use neutral lighting for material evaluation

### Success Criteria

The result must:

- Preserve the exact geometry from Phase 1
- Apply materials consistently across surfaces
- Produce believable surface detail without altering structure
- Maintain continuity across edges and corners
- Match the visual character of reference images (colors, textures, weathering)

**This phase concerns appearance only. No structural changes are allowed.**

### Phase 2 Approval Gate

Phase 2 is complete when:
1. All materials applied and verified in renders
2. User explicitly approves: **"Appearance is correct, proceed to Phase 3"**
3. Building (mesh + materials) is **FROZEN** - no further changes allowed

**Phase 2 must be approved before Phase 3 begins.**

---

## Phase 3 — Environment (SCENE COMPOSITION)

### Prerequisites

- **Phase 1 and Phase 2 APPROVED and FROZEN**
- Building may NOT be modified in Phase 3

### Outcome

Produce a **complete scene** by placing the building into a surrounding environment.

### What IS Included in Phase 3

- Ground surface and terrain
- Surrounding context (vegetation, debris, other elements)
- Lighting setup (time of day, shadows, atmosphere)
- Camera positioning for final presentation
- Any environmental effects (fog, haze, etc.)

### What IS NOT Included in Phase 3

- **NO building modifications** - geometry and materials are frozen
- Focus is entirely on context and presentation

### Success Criteria

The environment must:

- Establish correct scale and orientation
- Include ground, surrounding context, and lighting
- Allow a user to move through the space naturally
- Treat the building as a finished, immutable object
- Support the intended mood and character (creepy, abandoned aesthetic)

### Phase 3 Approval Gate

Phase 3 is complete when:
1. Environment and scene composition verified in renders
2. User explicitly approves: **"Scene is complete, project finished"**

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
3. Designing and executing whatever internal process is required to achieve **Phase 1 — Building Mesh**  
4. Proceeding autonomously until a decision or approval is required  
