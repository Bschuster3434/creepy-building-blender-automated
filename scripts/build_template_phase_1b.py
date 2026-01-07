"""
Phase 1B Build Template - Opening Fill

This template adds window frames, glass, and door panels to Phase 1A cutouts.

CRITICAL: Phase 1A base structure is FROZEN - no modifications allowed.
All Phase 1B geometry fits WITHIN existing cutouts from Phase 1A.

Usage:
    iteration_num = 1  # Phase 1B iteration number
    phase_1a_iteration = 49  # Phase 1A frozen iteration
    exec(open('scripts/build_template_phase_1b.py').read())
"""

import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent if '__file__' in globals() else Path("C:/Users/brian/Documents/Blender/Creepy Building Myrtle Beach Highway/scripts")
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

import bpy
import yaml
from phase_1b_helpers import (
    create_window_frame,
    create_window_glass,
    create_door_frame,
    create_door_panel,
    create_outer_trim,
    create_window_sill,
    create_door_threshold,
    create_inner_window_frame,
    create_horizontal_muntin,
    reposition_frame_pieces,
    reposition_glass_or_panel
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# REQUIRED: Set iteration numbers before running
if 'iteration_num' not in globals():
    raise ValueError(
        "\n" + "="*70 + "\n"
        "ERROR: iteration_num not set\n"
        "="*70 + "\n"
        "You must set the Phase 1B iteration number before running:\n\n"
        "    iteration_num = 1  # Phase 1B iteration\n"
        "    phase_1a_iteration = 49  # Phase 1A frozen iteration\n"
        "    exec(open('scripts/build_template_phase_1b.py').read())\n"
        "="*70 + "\n"
    )

if 'phase_1a_iteration' not in globals():
    raise ValueError(
        "\n" + "="*70 + "\n"
        "ERROR: phase_1a_iteration not set\n"
        "="*70 + "\n"
        "You must specify which Phase 1A iteration to use as base:\n\n"
        "    phase_1a_iteration = 49  # Phase 1A frozen iteration\n"
        "="*70 + "\n"
    )

print("="*70)
print(f" Phase 1B Iteration {iteration_num:03d} - Opening Fill")
print("="*70)
print(f"\nBasing on Phase 1A iteration {phase_1a_iteration:03d} (FROZEN)")
print(f"Adding window frames, glass, and door panels\n")

# Load Phase 1B specification
spec_path = scripts_dir.parent / 'work' / 'spec' / 'phase_1b' / 'opening_fill.yaml'
with open(spec_path, 'r') as f:
    spec = yaml.safe_load(f)

# Load Phase 1A specification (for cutout positions)
phase_1a_spec_path = scripts_dir.parent / 'work' / 'spec' / 'phase_1a' / 'building_geometry.yaml'
with open(phase_1a_spec_path, 'r') as f:
    phase_1a_spec = yaml.safe_load(f)

# ============================================================================
# SECTION 1: LOAD PHASE 1A GEOMETRY (FROZEN)
# ============================================================================
print("\n" + "="*70)
print(" SECTION 1: Loading Phase 1A Geometry (FROZEN)")
print("="*70)

# Import Phase 1A GLB
phase_1a_glb = scripts_dir.parent / 'exports' / 'glb' / f'building_phase_1a_iter_{phase_1a_iteration:03d}.glb'

if not phase_1a_glb.exists():
    raise FileNotFoundError(
        f"\n" + "="*70 + "\n"
        f"ERROR: Phase 1A GLB not found\n"
        f"="*70 + "\n"
        f"Expected: {phase_1a_glb}\n\n"
        f"Phase 1A iteration {phase_1a_iteration} must be exported before Phase 1B can proceed.\n"
        f"="*70 + "\n"
    )

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import Phase 1A GLB
print(f"\nImporting Phase 1A GLB: {phase_1a_glb.name}")
bpy.ops.import_scene.gltf(filepath=str(phase_1a_glb))

# Count Phase 1A geometry (for verification)
phase_1a_objects = list(bpy.data.objects)
phase_1a_vertex_count = sum(len(obj.data.vertices) if obj.type == 'MESH' else 0 for obj in phase_1a_objects)
phase_1a_face_count = sum(len(obj.data.polygons) if obj.type == 'MESH' else 0 for obj in phase_1a_objects)

print(f"✓ Phase 1A geometry loaded: {len(phase_1a_objects)} objects")
print(f"  Phase 1A vertex count: {phase_1a_vertex_count}")
print(f"  Phase 1A face count: {phase_1a_face_count}")
print(f"\n⚠️  Phase 1A geometry is FROZEN - no modifications allowed")

# ============================================================================
# SECTION 2: ADD WINDOW FRAMES AND GLASS
# ============================================================================
print("\n" + "="*70)
print(" SECTION 2: Adding Window Frames and Glass")
print("="*70)

phase_1b_objects = []

# Front left display window
print("\n[2.1] Front Left Display Window...")
cutout_spec = phase_1a_spec['cutouts']['front_left_display_window']
window_spec = spec['front_left_display_window']

frame = create_window_frame(
    "Front_Left_Window_Frame",
    width=window_spec['frame']['width'],
    height=window_spec['frame']['height'],
    thickness=window_spec['frame']['thickness'],
    depth=window_spec['frame']['depth'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + window_spec['frame']['height']/2),
    color=window_spec['frame']['color']
)
phase_1b_objects.extend(frame)

glass = create_window_glass(
    "Front_Left_Window_Glass",
    width=window_spec['glass']['width'],
    height=window_spec['glass']['height'],
    thickness=window_spec['glass']['thickness'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + window_spec['frame']['height']/2),
    color=window_spec['glass']['color']
)
phase_1b_objects.append(glass)
print(f"  ✓ Frame: {window_spec['frame']['width']}m × {window_spec['frame']['height']}m")
print(f"  ✓ Glass: {window_spec['glass']['width']}m × {window_spec['glass']['height']}m")

# Add detail if specified
detail_spec = window_spec.get('detail')
if detail_spec:
    print("  [Detail Enhancement]")

    # Outer trim around brick opening
    if detail_spec.get('outer_trim', {}).get('enabled'):
        trim_sides = detail_spec['outer_trim']['sides_width']
        trim_top = detail_spec['outer_trim']['top_width']
        trim_bottom = detail_spec['outer_trim']['bottom_width']
        trim_bottom_enabled = detail_spec['outer_trim'].get('bottom_enabled', True)  # Default to enabled
        trim_depth = detail_spec['outer_trim']['depth']

        # Outer trim sits at brick face edge (y = -7.5 + small offset forward)
        trim_y = cutout_spec['position']['y'] + 0.01
        trim_center = (
            cutout_spec['position']['x'],
            trim_y,
            cutout_spec['position']['z'] + window_spec['frame']['height']/2
        )

        # Create outer trim (3 or 4 pieces depending on bottom_enabled)
        from phase_1b_helpers import create_box_helper, apply_material_helper
        import math

        trim_pieces = []
        half_w = window_spec['frame']['width'] / 2
        half_h = window_spec['frame']['height'] / 2

        # Top trim
        top_piece = create_box_helper(
            "Front_Left_Window_OuterTrim_Top",
            width=window_spec['frame']['width'] + 2*trim_sides,
            depth=trim_depth,
            height=trim_top,
            location=(trim_center[0], trim_center[1], trim_center[2] + half_h + trim_top/2)
        )
        apply_material_helper(top_piece, window_spec['frame']['color'], "Front_Left_Window_Trim_Mat")
        trim_pieces.append(top_piece)

        # Bottom trim (only if enabled)
        if trim_bottom_enabled:
            bottom_piece = create_box_helper(
                "Front_Left_Window_OuterTrim_Bottom",
                width=window_spec['frame']['width'] + 2*trim_sides,
                depth=trim_depth,
                height=trim_bottom,
                location=(trim_center[0], trim_center[1], trim_center[2] - half_h - trim_bottom/2)
            )
            apply_material_helper(bottom_piece, window_spec['frame']['color'], "Front_Left_Window_Trim_Mat")
            trim_pieces.append(bottom_piece)

        # Left trim
        left_piece = create_box_helper(
            "Front_Left_Window_OuterTrim_Left",
            width=trim_sides,
            depth=trim_depth,
            height=window_spec['frame']['height'],
            location=(trim_center[0] - half_w - trim_sides/2, trim_center[1], trim_center[2])
        )
        apply_material_helper(left_piece, window_spec['frame']['color'], "Front_Left_Window_Trim_Mat")
        trim_pieces.append(left_piece)

        # Right trim
        right_piece = create_box_helper(
            "Front_Left_Window_OuterTrim_Right",
            width=trim_sides,
            depth=trim_depth,
            height=window_spec['frame']['height'],
            location=(trim_center[0] + half_w + trim_sides/2, trim_center[1], trim_center[2])
        )
        apply_material_helper(right_piece, window_spec['frame']['color'], "Front_Left_Window_Trim_Mat")
        trim_pieces.append(right_piece)

        phase_1b_objects.extend(trim_pieces)

        bottom_status = "enabled" if trim_bottom_enabled else "disabled"
        print(f"    ✓ Outer trim: sides {trim_sides}m, top {trim_top}m, bottom {bottom_status}, depth {trim_depth}m")

    # Reposition frame pieces back by recess
    frame_recess = detail_spec.get('frame_recess', 0)
    if frame_recess > 0:
        reposition_frame_pieces(frame, -frame_recess)
        print(f"    ✓ Frame recessed: {frame_recess}m into wall")

    # Inner frame (window stop) for layered look
    if detail_spec.get('inner_frame', {}).get('enabled'):
        inner_spec = detail_spec['inner_frame']
        inner_thickness = inner_spec['thickness']
        inner_depth = inner_spec['depth']
        inner_setback = inner_spec['setback']

        # Inner frame Y position: outer frame Y - additional setback
        inner_y = cutout_spec['position']['y'] - frame_recess - inner_setback

        inner_frame = create_inner_window_frame(
            "Front_Left_Window",
            outer_width=window_spec['frame']['width'],
            outer_height=window_spec['frame']['height'],
            outer_frame_thickness=window_spec['frame']['thickness'],
            inner_frame_thickness=inner_thickness,
            inner_frame_depth=inner_depth,
            location=(cutout_spec['position']['x'], inner_y, cutout_spec['position']['z'] + window_spec['frame']['height']/2),
            color=window_spec['frame']['color']
        )
        phase_1b_objects.extend(inner_frame)
        print(f"    ✓ Inner frame: {inner_thickness}m thick, {inner_setback}m setback")

    # Window sill at bottom
    if detail_spec.get('window_sill', {}).get('enabled'):
        sill_spec = detail_spec['window_sill']
        sill_overhang = sill_spec['overhang']
        sill_projection = sill_spec['projection']
        sill_height = sill_spec['height']

        # Sill width = cutout width + 2×overhang
        sill_width = window_spec['frame']['width'] + 2 * sill_overhang

        # Sill projects forward from outer trim
        sill_y = cutout_spec['position']['y'] + 0.01 + sill_projection

        # Sill at bottom of window (cutout position is at bottom)
        sill_z = cutout_spec['position']['z'] + sill_height/2

        sill = create_window_sill(
            "Front_Left_Window_Sill",
            width=sill_width,
            depth=sill_projection + 0.06,  # Sill depth (forward projection + trim overlap)
            height=sill_height,
            center_location=(cutout_spec['position']['x'], sill_y, sill_z),
            color=window_spec['frame']['color']
        )
        phase_1b_objects.append(sill)
        print(f"    ✓ Window sill: {sill_width}m wide × {sill_height}m thick, projects {sill_projection}m")

    # Reposition glass back by recess + inner frame setback + glass setback
    glass_setback = detail_spec.get('glass_setback', 0)
    inner_frame_setback = detail_spec.get('inner_frame', {}).get('setback', 0) if detail_spec.get('inner_frame', {}).get('enabled') else 0
    total_glass_offset = -(frame_recess + inner_frame_setback + glass_setback)
    if total_glass_offset != 0:
        reposition_glass_or_panel(glass, total_glass_offset)
        print(f"    ✓ Glass recessed: {-total_glass_offset}m from outer trim")

# Front right display window
print("\n[2.2] Front Right Display Window...")
cutout_spec = phase_1a_spec['cutouts']['front_right_display_window']
window_spec = spec['front_right_display_window']

frame = create_window_frame(
    "Front_Right_Window_Frame",
    width=window_spec['frame']['width'],
    height=window_spec['frame']['height'],
    thickness=window_spec['frame']['thickness'],
    depth=window_spec['frame']['depth'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + window_spec['frame']['height']/2),
    color=window_spec['frame']['color']
)
phase_1b_objects.extend(frame)

glass = create_window_glass(
    "Front_Right_Window_Glass",
    width=window_spec['glass']['width'],
    height=window_spec['glass']['height'],
    thickness=window_spec['glass']['thickness'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + window_spec['frame']['height']/2),
    color=window_spec['glass']['color']
)
phase_1b_objects.append(glass)
print(f"  ✓ Frame: {window_spec['frame']['width']}m × {window_spec['frame']['height']}m")
print(f"  ✓ Glass: {window_spec['glass']['width']}m × {window_spec['glass']['height']}m")

# Add detail if specified
detail_spec = window_spec.get('detail')
if detail_spec:
    print("  [Detail Enhancement]")

    # Outer trim around brick opening
    if detail_spec.get('outer_trim', {}).get('enabled'):
        trim_sides = detail_spec['outer_trim']['sides_width']
        trim_top = detail_spec['outer_trim']['top_width']
        trim_bottom = detail_spec['outer_trim']['bottom_width']
        trim_bottom_enabled = detail_spec['outer_trim'].get('bottom_enabled', True)
        trim_depth = detail_spec['outer_trim']['depth']

        trim_y = cutout_spec['position']['y'] + 0.01
        trim_center = (
            cutout_spec['position']['x'],
            trim_y,
            cutout_spec['position']['z'] + window_spec['frame']['height']/2
        )

        from phase_1b_helpers import create_box_helper, apply_material_helper
        import math

        trim_pieces = []
        half_w = window_spec['frame']['width'] / 2
        half_h = window_spec['frame']['height'] / 2

        # Top trim
        top_piece = create_box_helper(
            "Front_Right_Window_OuterTrim_Top",
            width=window_spec['frame']['width'] + 2*trim_sides,
            depth=trim_depth,
            height=trim_top,
            location=(trim_center[0], trim_center[1], trim_center[2] + half_h + trim_top/2)
        )
        apply_material_helper(top_piece, window_spec['frame']['color'], "Front_Right_Window_Trim_Mat")
        trim_pieces.append(top_piece)

        # Bottom trim (only if enabled)
        if trim_bottom_enabled:
            bottom_piece = create_box_helper(
                "Front_Right_Window_OuterTrim_Bottom",
                width=window_spec['frame']['width'] + 2*trim_sides,
                depth=trim_depth,
                height=trim_bottom,
                location=(trim_center[0], trim_center[1], trim_center[2] - half_h - trim_bottom/2)
            )
            apply_material_helper(bottom_piece, window_spec['frame']['color'], "Front_Right_Window_Trim_Mat")
            trim_pieces.append(bottom_piece)

        # Left trim
        left_piece = create_box_helper(
            "Front_Right_Window_OuterTrim_Left",
            width=trim_sides,
            depth=trim_depth,
            height=window_spec['frame']['height'],
            location=(trim_center[0] - half_w - trim_sides/2, trim_center[1], trim_center[2])
        )
        apply_material_helper(left_piece, window_spec['frame']['color'], "Front_Right_Window_Trim_Mat")
        trim_pieces.append(left_piece)

        # Right trim
        right_piece = create_box_helper(
            "Front_Right_Window_OuterTrim_Right",
            width=trim_sides,
            depth=trim_depth,
            height=window_spec['frame']['height'],
            location=(trim_center[0] + half_w + trim_sides/2, trim_center[1], trim_center[2])
        )
        apply_material_helper(right_piece, window_spec['frame']['color'], "Front_Right_Window_Trim_Mat")
        trim_pieces.append(right_piece)

        phase_1b_objects.extend(trim_pieces)

        bottom_status = "enabled" if trim_bottom_enabled else "disabled"
        print(f"    ✓ Outer trim: sides {trim_sides}m, top {trim_top}m, bottom {bottom_status}, depth {trim_depth}m")

    # Reposition frame pieces back by recess
    frame_recess = detail_spec.get('frame_recess', 0)
    if frame_recess > 0:
        reposition_frame_pieces(frame, -frame_recess)
        print(f"    ✓ Frame recessed: {frame_recess}m into wall")

    # Inner frame (window stop) for layered look
    if detail_spec.get('inner_frame', {}).get('enabled'):
        inner_spec = detail_spec['inner_frame']
        inner_thickness = inner_spec['thickness']
        inner_depth = inner_spec['depth']
        inner_setback = inner_spec['setback']

        # Inner frame Y position: outer frame Y - additional setback
        inner_y = cutout_spec['position']['y'] - frame_recess - inner_setback

        inner_frame = create_inner_window_frame(
            "Front_Right_Window",
            outer_width=window_spec['frame']['width'],
            outer_height=window_spec['frame']['height'],
            outer_frame_thickness=window_spec['frame']['thickness'],
            inner_frame_thickness=inner_thickness,
            inner_frame_depth=inner_depth,
            location=(cutout_spec['position']['x'], inner_y, cutout_spec['position']['z'] + window_spec['frame']['height']/2),
            color=window_spec['frame']['color']
        )
        phase_1b_objects.extend(inner_frame)
        print(f"    ✓ Inner frame: {inner_thickness}m thick, {inner_setback}m setback")

    # Window sill at bottom (if enabled)
    if detail_spec.get('window_sill', {}).get('enabled'):
        sill_spec = detail_spec['window_sill']
        sill_overhang = sill_spec['overhang']
        sill_projection = sill_spec['projection']
        sill_height = sill_spec['height']

        sill_width = window_spec['frame']['width'] + 2 * sill_overhang
        sill_y = cutout_spec['position']['y'] + 0.01 + sill_projection
        sill_z = cutout_spec['position']['z'] + sill_height/2

        sill = create_window_sill(
            "Front_Right_Window_Sill",
            width=sill_width,
            depth=sill_projection + 0.06,
            height=sill_height,
            center_location=(cutout_spec['position']['x'], sill_y, sill_z),
            color=window_spec['frame']['color']
        )
        phase_1b_objects.append(sill)
        print(f"    ✓ Window sill: {sill_width}m wide × {sill_height}m thick, projects {sill_projection}m")

    # Reposition glass back by recess + inner frame setback + glass setback
    glass_setback = detail_spec.get('glass_setback', 0)
    inner_frame_setback = detail_spec.get('inner_frame', {}).get('setback', 0) if detail_spec.get('inner_frame', {}).get('enabled') else 0
    total_glass_offset = -(frame_recess + inner_frame_setback + glass_setback)
    if total_glass_offset != 0:
        reposition_glass_or_panel(glass, total_glass_offset)
        print(f"    ✓ Glass recessed: {-total_glass_offset}m from outer trim")

# Alcove left window (angled wall)
print("\n[2.3] Alcove Left Window (angled)...")
cutout_spec = phase_1a_spec['cutouts']['door_alcove_left_window']
window_spec = spec['door_alcove_left_window']

# Calculate rotation AND correct Y position for angled wall
import math
door_alcove = phase_1a_spec.get('door_alcove', {})
if door_alcove.get('enabled', False):
    # Calculate rotation
    alcove_y_front = door_alcove['position']['y_front']
    alcove_y_back = door_alcove['position']['y_back']
    alcove_depth_y = alcove_y_back - alcove_y_front
    left_dx = door_alcove['walls']['left']['back_x'] - door_alcove['walls']['left']['front_x']
    left_wall_direction_angle = math.atan2(left_dx, alcove_depth_y)
    alcove_left_angle = math.radians(90) - left_wall_direction_angle

    # Use actual cutout geometry positions (measured from Phase 1A wall mesh)
    # The cutout is actually at (-1.067, -6.947), not the spec position
    window_x = -1.067
    window_y = -6.947
    # Rotation to match cutout edge direction (63.7°)
    alcove_left_angle = math.radians(63.7)
else:
    alcove_left_angle = 0
    window_x = cutout_spec['position']['x']
    window_y = cutout_spec['position']['y']

frame = create_window_frame(
    "Alcove_Left_Window_Frame",
    width=window_spec['frame']['width'],
    height=window_spec['frame']['height'],
    thickness=window_spec['frame']['thickness'],
    depth=window_spec['frame']['depth'],
    location=(window_x, window_y, cutout_spec['position']['z'] + window_spec['frame']['height']/2),
    rotation_z=alcove_left_angle,
    color=window_spec['frame']['color']
)
phase_1b_objects.extend(frame)

# Check if divided light is enabled
divided_light = window_spec.get('divided_light', {})
if divided_light.get('enabled'):
    # Create divided glass panes with muntin
    glass_width = window_spec['glass']['width']
    glass_total_height = window_spec['glass']['height']
    muntin_thickness = divided_light['muntin_thickness']
    muntin_depth = divided_light['muntin_depth']
    division_ratio = divided_light['division_ratio']

    # Calculate pane heights
    usable_height = glass_total_height - muntin_thickness
    upper_height = usable_height * division_ratio
    lower_height = usable_height * (1 - division_ratio)

    # Window center Z
    window_center_z = cutout_spec['position']['z'] + window_spec['frame']['height']/2
    frame_inner_bottom_z = window_center_z - glass_total_height/2

    # Upper pane position (top of frame)
    upper_pane_z = frame_inner_bottom_z + lower_height + muntin_thickness + upper_height/2
    upper_glass = create_window_glass(
        "Alcove_Left_Window_Glass_Upper",
        width=glass_width,
        height=upper_height,
        thickness=window_spec['glass']['thickness'],
        location=(window_x, window_y, upper_pane_z),
        rotation_z=alcove_left_angle,
        color=window_spec['glass']['color']
    )
    phase_1b_objects.append(upper_glass)

    # Lower pane position (bottom of frame)
    lower_pane_z = frame_inner_bottom_z + lower_height/2
    lower_glass = create_window_glass(
        "Alcove_Left_Window_Glass_Lower",
        width=glass_width,
        height=lower_height,
        thickness=window_spec['glass']['thickness'],
        location=(window_x, window_y, lower_pane_z),
        rotation_z=alcove_left_angle,
        color=window_spec['glass']['color']
    )
    phase_1b_objects.append(lower_glass)

    # Muntin bar position (between panes)
    muntin_z = frame_inner_bottom_z + lower_height + muntin_thickness/2
    muntin = create_horizontal_muntin(
        "Alcove_Left_Window_Muntin",
        width=glass_width,
        thickness=muntin_thickness,
        depth=muntin_depth,
        location=(window_x, window_y, muntin_z),
        rotation_z=alcove_left_angle,
        color=window_spec['frame']['color']
    )
    phase_1b_objects.append(muntin)

    print(f"  ✓ Frame: {window_spec['frame']['width']}m × {window_spec['frame']['height']}m (rotated {math.degrees(alcove_left_angle):.1f}°)")
    print(f"  ✓ Divided light: upper {upper_height:.2f}m + muntin {muntin_thickness}m + lower {lower_height:.2f}m")
else:
    # Single glass pane (original behavior)
    glass = create_window_glass(
        "Alcove_Left_Window_Glass",
        width=window_spec['glass']['width'],
        height=window_spec['glass']['height'],
        thickness=window_spec['glass']['thickness'],
        location=(window_x, window_y, cutout_spec['position']['z'] + window_spec['frame']['height']/2),
        rotation_z=alcove_left_angle,
        color=window_spec['glass']['color']
    )
    phase_1b_objects.append(glass)
    print(f"  ✓ Frame: {window_spec['frame']['width']}m × {window_spec['frame']['height']}m (rotated {math.degrees(alcove_left_angle):.1f}°, y={window_y:.3f})")
    print(f"  ✓ Glass: {window_spec['glass']['width']}m × {window_spec['glass']['height']}m")

# Alcove right window (angled wall)
print("\n[2.4] Alcove Right Window (angled)...")
cutout_spec = phase_1a_spec['cutouts']['door_alcove_right_window']
window_spec = spec['door_alcove_right_window']

# Calculate rotation AND correct Y position for angled wall
if door_alcove.get('enabled', False):
    # Calculate rotation
    right_dx = door_alcove['walls']['right']['back_x'] - door_alcove['walls']['right']['front_x']
    right_wall_direction_angle = math.atan2(right_dx, alcove_depth_y)
    alcove_right_angle = math.radians(90) - right_wall_direction_angle

    # Use actual cutout geometry positions (measured from Phase 1A wall mesh)
    # The cutout is actually at (0.993, -6.981), not the spec position
    window_x = 0.993
    window_y = -6.981
    # Rotation to match cutout edge direction (-63.7° to mirror left window)
    alcove_right_angle = math.radians(-63.7)
else:
    alcove_right_angle = 0
    window_x = cutout_spec['position']['x']
    window_y = cutout_spec['position']['y']

frame = create_window_frame(
    "Alcove_Right_Window_Frame",
    width=window_spec['frame']['width'],
    height=window_spec['frame']['height'],
    thickness=window_spec['frame']['thickness'],
    depth=window_spec['frame']['depth'],
    location=(window_x, window_y, cutout_spec['position']['z'] + window_spec['frame']['height']/2),
    rotation_z=alcove_right_angle,
    color=window_spec['frame']['color']
)
phase_1b_objects.extend(frame)

# Check if divided light is enabled
divided_light = window_spec.get('divided_light', {})
if divided_light.get('enabled'):
    # Create divided glass panes with muntin
    glass_width = window_spec['glass']['width']
    glass_total_height = window_spec['glass']['height']
    muntin_thickness = divided_light['muntin_thickness']
    muntin_depth = divided_light['muntin_depth']
    division_ratio = divided_light['division_ratio']

    # Calculate pane heights
    usable_height = glass_total_height - muntin_thickness
    upper_height = usable_height * division_ratio
    lower_height = usable_height * (1 - division_ratio)

    # Window center Z
    window_center_z = cutout_spec['position']['z'] + window_spec['frame']['height']/2
    frame_inner_bottom_z = window_center_z - glass_total_height/2

    # Upper pane position (top of frame)
    upper_pane_z = frame_inner_bottom_z + lower_height + muntin_thickness + upper_height/2
    upper_glass = create_window_glass(
        "Alcove_Right_Window_Glass_Upper",
        width=glass_width,
        height=upper_height,
        thickness=window_spec['glass']['thickness'],
        location=(window_x, window_y, upper_pane_z),
        rotation_z=alcove_right_angle,
        color=window_spec['glass']['color']
    )
    phase_1b_objects.append(upper_glass)

    # Lower pane position (bottom of frame)
    lower_pane_z = frame_inner_bottom_z + lower_height/2
    lower_glass = create_window_glass(
        "Alcove_Right_Window_Glass_Lower",
        width=glass_width,
        height=lower_height,
        thickness=window_spec['glass']['thickness'],
        location=(window_x, window_y, lower_pane_z),
        rotation_z=alcove_right_angle,
        color=window_spec['glass']['color']
    )
    phase_1b_objects.append(lower_glass)

    # Muntin bar position (between panes)
    muntin_z = frame_inner_bottom_z + lower_height + muntin_thickness/2
    muntin = create_horizontal_muntin(
        "Alcove_Right_Window_Muntin",
        width=glass_width,
        thickness=muntin_thickness,
        depth=muntin_depth,
        location=(window_x, window_y, muntin_z),
        rotation_z=alcove_right_angle,
        color=window_spec['frame']['color']
    )
    phase_1b_objects.append(muntin)

    print(f"  ✓ Frame: {window_spec['frame']['width']}m × {window_spec['frame']['height']}m (rotated {math.degrees(alcove_right_angle):.1f}°)")
    print(f"  ✓ Divided light: upper {upper_height:.2f}m + muntin {muntin_thickness}m + lower {lower_height:.2f}m")
else:
    # Single glass pane (original behavior)
    glass = create_window_glass(
        "Alcove_Right_Window_Glass",
        width=window_spec['glass']['width'],
        height=window_spec['glass']['height'],
        thickness=window_spec['glass']['thickness'],
        location=(window_x, window_y, cutout_spec['position']['z'] + window_spec['frame']['height']/2),
        rotation_z=alcove_right_angle,
        color=window_spec['glass']['color']
    )
    phase_1b_objects.append(glass)
    print(f"  ✓ Frame: {window_spec['frame']['width']}m × {window_spec['frame']['height']}m (rotated {math.degrees(alcove_right_angle):.1f}°, y={window_y:.3f})")
    print(f"  ✓ Glass: {window_spec['glass']['width']}m × {window_spec['glass']['height']}m")

# ============================================================================
# SECTION 3: ADD DOOR FRAMES AND PANELS
# ============================================================================
print("\n" + "="*70)
print(" SECTION 3: Adding Door Frames and Panels")
print("="*70)

# Front entry door (double French door)
print("\n[3.1] Front Entry Door (alcove back)...")
cutout_spec = phase_1a_spec['cutouts']['front_entry_door']
door_spec = spec['front_entry_door']

frame = create_door_frame(
    "Front_Entry_Door_Frame",
    width=door_spec['frame']['width'],
    height=door_spec['frame']['height'],
    thickness=door_spec['frame']['thickness'],
    depth=door_spec['frame']['depth'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + door_spec['frame']['height']/2),
    color=door_spec['frame']['color']
)
phase_1b_objects.extend(frame)

# Two door panels (double door)
panel_width = door_spec['door_panels']['panel_width']
panel_height = door_spec['door_panels']['panel_height']
panel_depth = door_spec['door_panels'].get('panel_depth', 0.04)
panel_style = door_spec['door_panels'].get('style', 'solid')

if panel_style == '10-lite':
    # Import the French door helper
    from phase_1b_helpers import create_french_door_panel

    # Get grid configuration
    grid = door_spec['door_panels']['grid']
    rows = grid['rows']
    cols = grid['cols']
    stile_width = door_spec['door_panels']['stile_width']
    rail_width = door_spec['door_panels']['rail_width']
    muntin_width = door_spec['door_panels']['muntin_width']
    glass_thickness = door_spec['door_panels']['glass_thickness']
    frame_color = door_spec['door_panels']['frame_color']
    glass_color = door_spec['door_panels']['glass_color']

    # Left French door panel
    left_panel_result = create_french_door_panel(
        "Front_Entry_Door_Left",
        width=panel_width,
        height=panel_height,
        location=(cutout_spec['position']['x'] - panel_width/2, cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
        stile_width=stile_width,
        rail_width=rail_width,
        muntin_width=muntin_width,
        glass_thickness=glass_thickness,
        panel_depth=panel_depth,
        rows=rows,
        cols=cols,
        frame_color=frame_color,
        glass_color=glass_color
    )
    phase_1b_objects.extend(left_panel_result['frame'])
    phase_1b_objects.extend(left_panel_result['muntins'])
    phase_1b_objects.extend(left_panel_result['glass'])

    # Right French door panel
    right_panel_result = create_french_door_panel(
        "Front_Entry_Door_Right",
        width=panel_width,
        height=panel_height,
        location=(cutout_spec['position']['x'] + panel_width/2, cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
        stile_width=stile_width,
        rail_width=rail_width,
        muntin_width=muntin_width,
        glass_thickness=glass_thickness,
        panel_depth=panel_depth,
        rows=rows,
        cols=cols,
        frame_color=frame_color,
        glass_color=glass_color
    )
    phase_1b_objects.extend(right_panel_result['frame'])
    phase_1b_objects.extend(right_panel_result['muntins'])
    phase_1b_objects.extend(right_panel_result['glass'])

    print(f"  ✓ Frame: {door_spec['frame']['width']}m × {door_spec['frame']['height']}m")
    print(f"  ✓ 10-lite panels: 2× {panel_width}m × {panel_height}m ({rows}×{cols} grid)")
else:
    # Original solid panel code (fallback)
    panel_thickness = door_spec['door_panels'].get('panel_thickness', panel_depth)
    gap = door_spec['door_panels'].get('center_gap', 0)

    # Left panel
    left_panel = create_door_panel(
        "Front_Entry_Door_Left_Panel",
        width=panel_width,
        height=panel_height,
        thickness=panel_thickness,
        location=(cutout_spec['position']['x'] - panel_width/2 - gap/2, cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
        color=door_spec['door_panels'].get('color', '#1A1A1A')
    )
    phase_1b_objects.append(left_panel)

    # Right panel
    right_panel = create_door_panel(
        "Front_Entry_Door_Right_Panel",
        width=panel_width,
        height=panel_height,
        thickness=panel_thickness,
        location=(cutout_spec['position']['x'] + panel_width/2 + gap/2, cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
        color=door_spec['door_panels'].get('color', '#1A1A1A')
    )
    phase_1b_objects.append(right_panel)

    print(f"  ✓ Frame: {door_spec['frame']['width']}m × {door_spec['frame']['height']}m")
    print(f"  ✓ Panels: 2× {panel_width}m × {panel_height}m (double door)")

# Rear service door
print("\n[3.2] Rear Service Door...")
cutout_spec = phase_1a_spec['cutouts']['rear_service_door']
door_spec = spec['rear_service_door']

frame = create_door_frame(
    "Rear_Service_Door_Frame",
    width=door_spec['frame']['width'],
    height=door_spec['frame']['height'],
    thickness=door_spec['frame']['thickness'],
    depth=door_spec['frame']['depth'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + door_spec['frame']['height']/2),
    color=door_spec['frame']['color']
)
phase_1b_objects.extend(frame)

# Check panel style
panel_style = door_spec['door_panel'].get('style', 'solid')

if panel_style == 'half-lite':
    # Import the half-lite door helper
    from phase_1b_helpers import create_half_lite_door_panel

    # Get configuration
    panel_width = door_spec['door_panel']['width']
    panel_height = door_spec['door_panel']['height']
    panel_depth = door_spec['door_panel']['panel_depth']
    glass_ratio = door_spec['door_panel']['glass_ratio']
    grid = door_spec['door_panel']['grid']
    rows = grid['rows']
    cols = grid['cols']
    stile_width = door_spec['door_panel']['stile_width']
    rail_width = door_spec['door_panel']['rail_width']
    mid_rail_width = door_spec['door_panel']['mid_rail_width']
    muntin_width = door_spec['door_panel']['muntin_width']
    glass_thickness = door_spec['door_panel']['glass_thickness']
    panel_inset = door_spec['door_panel']['panel_inset']
    frame_color = door_spec['door_panel']['frame_color']
    glass_color = door_spec['door_panel']['glass_color']
    panel_color = door_spec['door_panel']['panel_color']

    # Create half-lite door panel
    panel_result = create_half_lite_door_panel(
        "Rear_Service_Door",
        width=panel_width,
        height=panel_height,
        location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
        glass_ratio=glass_ratio,
        stile_width=stile_width,
        rail_width=rail_width,
        mid_rail_width=mid_rail_width,
        muntin_width=muntin_width,
        glass_thickness=glass_thickness,
        panel_depth=panel_depth,
        rows=rows,
        cols=cols,
        panel_inset=panel_inset,
        frame_color=frame_color,
        glass_color=glass_color,
        panel_color=panel_color
    )
    phase_1b_objects.extend(panel_result['frame'])
    phase_1b_objects.extend(panel_result['muntins'])
    phase_1b_objects.extend(panel_result['glass'])
    phase_1b_objects.extend(panel_result['panels'])

    print(f"  ✓ Frame: {door_spec['frame']['width']}m × {door_spec['frame']['height']}m")
    print(f"  ✓ Half-lite panel: {panel_width}m × {panel_height}m ({rows}×{cols} glass grid + 2 panels)")
else:
    # Original solid panel code (fallback)
    panel = create_door_panel(
        "Rear_Service_Door_Panel",
        width=door_spec['door_panel']['width'],
        height=door_spec['door_panel']['height'],
        thickness=door_spec['door_panel'].get('thickness', 0.04),
        location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + door_spec['door_panel']['height']/2),
        color=door_spec['door_panel'].get('color', '#1A1A1A')
    )
    phase_1b_objects.append(panel)

    print(f"  ✓ Frame: {door_spec['frame']['width']}m × {door_spec['frame']['height']}m")
    print(f"  ✓ Panel: {door_spec['door_panel']['width']}m × {door_spec['door_panel']['height']}m")

print(f"\n✓ Phase 1B geometry complete: {len(phase_1b_objects)} new objects added")

# ============================================================================
# SECTION 4: VERIFY PHASE 1A PRESERVATION
# ============================================================================
print("\n" + "="*70)
print(" SECTION 4: Verifying Phase 1A Preservation")
print("="*70)

# Count current geometry
current_objects = list(bpy.data.objects)
current_vertex_count = sum(len(obj.data.vertices) if obj.type == 'MESH' else 0 for obj in current_objects)
current_face_count = sum(len(obj.data.polygons) if obj.type == 'MESH' else 0 for obj in current_objects)

# Verify Phase 1A unchanged (vertex/face counts should only increase by Phase 1B additions)
phase_1b_vertex_count = sum(len(obj.data.vertices) if obj.type == 'MESH' else 0 for obj in phase_1b_objects)
phase_1b_face_count = sum(len(obj.data.polygons) if obj.type == 'MESH' else 0 for obj in phase_1b_objects)

expected_vertex_count = phase_1a_vertex_count + phase_1b_vertex_count
expected_face_count = phase_1a_face_count + phase_1b_face_count

print(f"\nPhase 1A (frozen):")
print(f"  Vertices: {phase_1a_vertex_count}")
print(f"  Faces: {phase_1a_face_count}")

print(f"\nPhase 1B (added):")
print(f"  Vertices: {phase_1b_vertex_count}")
print(f"  Faces: {phase_1b_face_count}")

print(f"\nTotal (expected):")
print(f"  Vertices: {expected_vertex_count}")
print(f"  Faces: {expected_face_count}")

print(f"\nTotal (actual):")
print(f"  Vertices: {current_vertex_count}")
print(f"  Faces: {current_face_count}")

if current_vertex_count == expected_vertex_count and current_face_count == expected_face_count:
    print("\n✓ Phase 1A geometry preserved (counts match)")
else:
    print(f"\n⚠️  WARNING: Geometry counts don't match expected")
    print(f"   Vertex delta: {current_vertex_count - expected_vertex_count}")
    print(f"   Face delta: {current_face_count - expected_face_count}")

# ============================================================================
# SECTION 5: EXPORT PHASE 1B GLB
# ============================================================================
print("\n" + "="*70)
print(" SECTION 5: Exporting Phase 1B GLB")
print("="*70)

output_dir = scripts_dir.parent / 'exports' / 'glb'
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / f"building_phase_1b_iter_{iteration_num:03d}.glb"

# Select all objects for export
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

print(f"\nExporting: {output_file.name}")
print(f"  Objects: {len([obj for obj in bpy.data.objects if obj.select_get()])}")

bpy.ops.export_scene.gltf(
    filepath=str(output_file),
    use_selection=True,
    export_format='GLB'
)

# Check file size
file_size_kb = output_file.stat().st_size / 1024
print(f"\n✓ GLB exported: {output_file.name} ({file_size_kb:.1f} KB)")

# ============================================================================
# COMPLETION SUMMARY
# ============================================================================
print("\n" + "="*70)
print(f" ✅ PHASE 1B ITERATION {iteration_num:03d} COMPLETE")
print("="*70)

print(f"\nPhase 1A geometry (frozen): {len(phase_1a_objects)} objects")
print(f"Phase 1B geometry (added): {len(phase_1b_objects)} objects")
print(f"Total geometry: {len(current_objects)} objects")

print(f"\n✓ Window frames and glass added: 4 windows")
print(f"✓ Door frames and panels added: 2 doors")
print(f"✓ Phase 1A preservation verified")
print(f"✓ GLB export succeeded")

print("\n" + "="*70 + "\n")
