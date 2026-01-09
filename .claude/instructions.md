# Creepy Building - Project Instructions

## Core Principle: Baseline + Delta (NOT Fresh Builds)

**CRITICAL RULE FROM USER:**
> "Unless I explicitly talk about it, it must not be changed. If I do not explicitly mention something from the previous iteration, it must not be changed."

### What This Means:
- Each iteration is **incremental changes** to a baseline, NOT a fresh rebuild
- If a feature exists and user doesn't mention it → **KEEP IT UNCHANGED**
- Only modify what user explicitly requests
- Track baseline features in `work/iteration_state.yaml`

---

## Iteration Workflow

### When User Says "Make This Change"

1. **Identify ONLY what is being changed**
   - Read user request carefully
   - Change ONLY the specified element
   - Do NOT touch anything else

2. **Preserve baseline**
   - Check `work/iteration_state.yaml` for existing features
   - Keep all baseline features unless explicitly told to change them

3. **Rapid iteration**
   - One change at a time
   - Build → Verify → Export → Screenshot
   - Increment iteration number
   - Move to next change

4. **Verify no unintended changes**
   - Check verification report for unexpected dimension changes
   - Confirm only the requested element changed

---

## Architecture Feature Implementation (CRITICAL - Prevents Major Mistakes)

### BEFORE Implementing ANY Feature With Depth or Angles

**Problem:** 2D photos can be misinterpreted as 3D geometry
**Example:** Door alcove interpreted as rectangular recess when photos showed angled walls

**REQUIRED STEPS:**

#### Step 1: Analyze 3D Geometry from Photos
Ask yourself:
- What is the shape when viewed FROM ABOVE (plan view)?
  - Rectangle? Trapezoid? L-shape? Angled?
- Are walls PERPENDICULAR to facade or ANGLED?
  - If angled: inward or outward?
- What are the key dimensions?
  - Front opening width
  - Back opening width (if different from front)
  - Depth
  - Angles (if not 90 degrees)

#### Step 2: Describe Geometry in Plain Language
Write a description like:
```
Door alcove geometry:
- Plan view shape: TRAPEZOID (wide at front, narrow at back)
- Front opening: 4m wide at facade
- Back opening: 1.2m wide (door width)
- Depth: 1.4m
- Side walls: ANGLED inward (not perpendicular)
- Creates funnel/V-shape
```

#### Step 3: Verify Understanding BEFORE Building
If feature has:
- Angled walls (not perpendicular)
- Estimated dimensions
- Multiple possible interpretations

→ **ASK USER TO CONFIRM** geometry interpretation with your description and questions

#### Step 4: Only Then Implement
Add to spec, update build template, build iteration

**DO NOT assume rectangular/perpendicular geometry without verification**

---

## Lessons Learned (Historical Mistakes to Avoid)

### Iteration 005 Errors

**Error 1: Removed working features not mentioned in feedback**
- Parapet was in iteration 004 (working)
- User didn't mention parapet in feedback
- I removed it (treating as fresh build instead of incremental)
- **Fix:** Check `iteration_state.yaml` for baseline features, preserve unless told to change

**Error 2: Added unrequested features from spec**
- Back door and side windows in spec but never requested by user
- I built them because they were in spec
- **Fix:** Deleted unrequested features from spec entirely (don't mark as "requested: false")

**Error 3: Removed structural elements based on misunderstanding**
- User said "posts should be at edges"
- I interpreted as "ONLY at edges" and removed center post
- Center post was structural (holds beam)
- **Fix:** Center post is structural requirement, keep unless explicitly told to remove

**Error 4: Window clearance calculation**
- Raised window sill but didn't check clearance to canopy
- Windows intersected canopy
- **Fix:** Always calculate clearances for overlapping elements

### Iteration 008 Error

**Error: Door alcove geometry misinterpreted**
- Reference photo showed ANGLED walls (trapezoidal plan)
- I implemented RECTANGULAR recess (perpendicular walls)
- Assumed simple shape without analyzing plan view
- **Fix:** Use "Architecture Feature Implementation" process above

### Iterations 008-011 Error

**Error: Not using visual verification capability**
- I have multimodal capability (can see and analyze images)
- Was taking screenshots but NOT analyzing what I saw in them
- Treated screenshots as a checkbox for user only, not as verification step
- User identified: "it doesn't seem to be working very well"
- **Fix:** Added "Visual Verification" as required step in process (see Verification Requirements section)

---

## Coordinate System

- Z=0 is at **wall base** (top of foundation), NOT ground
- Foundation extends from Z=-0.28 to Z=0
- Walls start at Z=0 and go up to Z=3.75
- Roof top at Z=3.95 (3.75 wall + 0.20 roof thickness)
- Parapets measured from roof top (Z=3.95)

---

## Spec File Rules

### Unrequested Features
- If user never requested a feature: **DELETE it from spec**
- Do NOT mark as "requested: false" - just remove the entry
- Only include features user has explicitly requested

### Validation Targets
- Must match what is actually built
- Update when features change
- Used by verification scripts

---

## Verification Requirements

Every iteration MUST pass **TWO types of verification:**

### 1. Automated Verification (Required Gates)
Every iteration MUST pass:
1. Inline verification (checkpoint 1)
2. Batch verification (checkpoint 2)
3. Automated verification (checkpoint 3)

Export is BLOCKED until all 3 checkpoints exist.

### 2. Visual Verification (CRITICAL - Use Multimodal Capability)

**Problem:** I have multimodal capability (can see images) but was NOT using it to verify changes.
**User identified:** "it doesn't seem to be working very well" - because I was taking screenshots as a checkbox without analyzing them.

**REQUIRED PROCESS:**

#### Step 1: Take Screenshot from Relevant Angle
- If change is on front facade → screenshot from front
- If change is structural/depth-related → screenshot from angle showing depth
- Match camera angle to reference photos when possible

#### Step 2: ACTUALLY LOOK AT THE SCREENSHOT
**This is NOT a checkbox - I must visually analyze what I see:**
- Does the changed feature look correct?
- Are proportions reasonable?
- Are there any obvious intersections/overlaps?
- Does it match what the user requested?

#### Step 3: Compare to Reference Photos (When Applicable)
If implementing from reference photos:
- Load reference photo and screenshot side-by-side (conceptually)
- Compare angles, proportions, relationships
- Ask: "Does my implementation capture the geometry I see in the reference?"
- Note: Not expecting pixel-perfect match, but geometry should be comparable

#### Step 4: Report Visual Findings
**In my response to user, I must report:**
- What I see in the screenshot
- Whether it matches the user's request
- Any concerns or potential issues noticed
- Comparison to reference photos (if applicable)

**Example:**
```
Visual verification:
- Screenshot shows angled alcove walls creating trapezoid shape ✓
- Alcove front opening appears ~2.5m wide, proper gap from windows ✓
- Door visible recessed at back of alcove ✓
- Compared to reference photo: angle and proportions match ✓
- No obvious intersections or geometry errors ✓
```

**DO NOT:**
- Take screenshot and ignore what's in it
- Treat screenshots as a checkbox for the user only
- Skip visual verification because "automated tests passed"

**I AM MULTIMODAL - I CAN AND MUST USE THIS CAPABILITY**

---

## File References

- **Baseline features:** `work/iteration_state.yaml`
- **Geometry spec:** `work/spec/phase_1a/building_geometry.yaml`
- **Build template:** `scripts/build_template_phase_1a.py`
- **Verification:** `scripts/verify_phase_1a.py`

---

## Quick Checklist Before Each Iteration

**Before Building:**
- [ ] Read user request - what SPECIFICALLY are they asking to change?
- [ ] Check `iteration_state.yaml` - what baseline features exist?
- [ ] Is feature architectural with depth/angles? → Use geometry analysis process
- [ ] Implement ONLY the requested change

**After Building:**
- [ ] Automated verification - all 3 checkpoints passed?
- [ ] Verify no other dimensions changed
- [ ] Export GLB file
- [ ] Take screenshot from appropriate angle
- [ ] **VISUAL VERIFICATION - Actually analyze the screenshot:**
  - Does it match what user requested?
  - Any intersections/overlaps/errors visible?
  - Compare to reference photos if applicable
  - Report what I see to user
- [ ] Ready for next change
