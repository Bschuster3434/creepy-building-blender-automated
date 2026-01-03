# Iteration Decision: 001 → 002

**Decision Date**: 2026-01-02
**Decision**: **ITERATE** → Proceed to Iteration 002

---

## Current State

- **Iteration**: 001
- **Spec version**: v002
- **Convergence**: 45%
- **Status**: NEEDS IMPROVEMENT
- **Phase**: Phase 1 - Building Mesh

---

## Issue Analysis

### Critical Issues (All Fixable)

#### 1. Missing Parapet Corner Steps
- **Status**: CAN FIX
- **Current**: Only 6 corner step assemblies created
- **Required**: 8 corner step assemblies (L-shaped building has 8 convex corners)
- **Proposed Fix**: Update spec to explicitly define all 8 corner positions
- **Expected Impact**: Completes defining architectural feature, +10% convergence

#### 2. Oversized Canopy Beam
- **Status**: CAN FIX
- **Current**: Beam too large, positioned incorrectly above canopy roof
- **Required**: Thin I-beam (~0.15m depth) flush with or below canopy underside
- **Proposed Fix**: Reduce beam dimensions, correct vertical positioning
- **Expected Impact**: Fixes major front facade proportion issue, +8% convergence

#### 3. Chimney Position Wrong
- **Status**: CAN FIX
- **Current**: Chimney at Y ~6.0m (too far back)
- **Required**: Chimney at Y ~5.0-5.5m (more centered)
- **Proposed Fix**: Update chimney.position.y from 6.0 to 5.25
- **Expected Impact**: Better matches overhead references, +5% convergence

#### 4. Canopy Post Alignment
- **Status**: CAN FIX
- **Current**: Posts obscured or positioned incorrectly
- **Required**: Posts clearly visible at front edge of canopy
- **Proposed Fix**: Verify post Y positions, ensure no geometry occlusion
- **Expected Impact**: Improves front facade clarity, +5% convergence

---

### Major Issues (Prioritized Top 5)

#### 5. Window Proportions Too Narrow
- **Status**: CAN FIX
- **Current**: 2.3m width
- **Suggested**: 2.4-2.5m width
- **Expected Impact**: Better storefront appearance, +3% convergence

#### 6. Parapet Height Too Low
- **Status**: CAN FIX
- **Current**: 0.70m
- **Suggested**: 0.80m
- **Expected Impact**: Better proportions, +3% convergence

#### 7. Extension Depth Too Long
- **Status**: CAN FIX
- **Current**: 3.5m
- **Suggested**: 3.0m
- **Expected Impact**: More compact L-shape, +2% convergence

#### 8. Side Wall Openings Missing
- **Status**: CAN FIX
- **Current**: Defined in spec but not visible in renders
- **Suggested**: Ensure geometry generation creates them
- **Expected Impact**: Adds detail, +2% convergence

#### 9. Material Placeholders
- **Status**: PHASE 2 CONCERN
- **Note**: Basic materials are expected for Phase 1
- **Action**: Document but defer to Phase 2

---

## Decision: ITERATE

### Rationale

1. **All critical issues are fixable** - No user input required, all fixes are clear geometric adjustments
2. **Clear path to improvement** - Specific dimensional values and changes identified
3. **Strong foundation** - 45% convergence with solid L-shaped footprint and all major elements present
4. **Predictable outcome** - Fixes are straightforward and should yield measurable improvement
5. **No blockers** - No ambiguities, contradictions, or missing data

### Expected Outcome After Iteration 002

- **Estimated convergence**: 70-75%
- **Issues expected to be resolved**:
  - 4 critical issues → 0 critical
  - 4 major geometric issues → 1-2 major
  - Minor issues remain for fine-tuning

- **Remaining issues**:
  - Minor dimensional tweaks
  - Cosmetic material concerns (Phase 2)

---

## Next Steps

### 1. Update Spec: v002 → v003

Make the following changes to `work/spec/building_v002.yaml`:

#### Geometry Fixes (Critical)

**A. Parapet Corner Steps** (Add 2 missing corners)
```yaml
parapet:
  corner_steps:
    corners: 8  # Explicitly specify all 8 corners
    # Define all corner positions for L-shaped building
```

**B. Canopy Beam Dimensions**
```yaml
canopy:
  beam:
    height: 0.15  # Reduce from oversized to I-beam proportion
    width: 0.10
    position_z: 3.15  # Flush with canopy underside (2.85 + 0.35 - 0.05)
```

**C. Chimney Position**
```yaml
chimney:
  position:
    x: 2.5
    y: 5.25  # Move from 6.0 to 5.25 (more centered)
    z: 3.95
```

**D. Canopy Posts** (Verify positioning)
```yaml
canopy:
  support_posts:
    # Verify Y position ensures visibility at front edge
    positions: [each post at y: -2.75]
```

#### Dimensional Refinements (Major)

**E. Display Windows**
```yaml
openings:
  windows:
    - id: F-02_left_display
      width: 2.45  # Increase from 2.3
    - id: F-03_right_display
      width: 2.45  # Increase from 2.3
```

**F. Parapet Height**
```yaml
parapet:
  height: 0.80  # Increase from 0.70
overall:
  height:
    parapet_height: 0.80
    total_height: 4.55  # Update: 3.75 + 0.80
```

**G. Extension Depth**
```yaml
footprint_geometry:
  extension_rectangle:
    depth: 3.0  # Reduce from 3.5
```

#### Minor Refinements

**H. Additional Tweaks**
- Foundation exposed height: 0.35 → 0.28
- Door height: 2.1 → 2.05
- Chimney height above parapet: 0.75 → 0.90

### 2. Validate Spec v003
- Run Quality Gatekeeper Agent on v003
- Ensure all schema requirements met
- Verify internal consistency

### 3. Build Geometry: Iteration 002
- Run Blender Operator Agent with v003
- Generate all geometry with fixes applied
- Export GLB: `building_iter_002.glb`

### 4. Render Standard Views
- Generate 6 renders: front, left, right, rear, iso, top
- Save to: `work/renders/iter_002/`

### 5. Generate Critique
- Run Visual Critic Agent
- Compare iter_002 renders to references
- Assess convergence improvement
- Output: `work/reviews/critique_002.json`

### 6. Reassess Convergence
- Expected: 70-75%
- If ≥ 85%: Recommend Phase 1 approval
- If 70-84%: Plan iteration 003 with remaining minor fixes
- If < 70%: Investigate why fixes didn't achieve expected improvement

---

## Confidence Level: **HIGH**

**Reasoning**:
1. All issues have clear, unambiguous fixes
2. Fixes are incremental adjustments, not redesigns
3. No dependencies between fixes that could create conflicts
4. Reference images provide clear targets for all adjustments
5. First iteration established solid foundation to build upon

**Risk**: Low - Worst case is convergence improves to 60-65% instead of 70-75%, still progress in right direction

---

## Agent Assignments

1. **Spec Architect Agent** - Update v002 → v003 with all fixes listed above
2. **Quality Gatekeeper Agent** - Validate v003
3. **Blender Operator Agent** - Build iter_002 from v003
4. **Visual Critic Agent** - Critique iter_002 renders
5. **Iteration Orchestrator** - Reassess after iter_002 completes

---

## Success Metrics for Iteration 002

- [ ] All 8 parapet corner steps present
- [ ] Canopy beam properly proportioned and positioned
- [ ] Chimney at correct Y position
- [ ] Canopy posts clearly visible
- [ ] Window widths increased
- [ ] Parapet height increased
- [ ] Extension depth reduced
- [ ] Convergence ≥ 70%
- [ ] Zero critical issues remaining
- [ ] ≤ 2 major issues remaining
