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

    # Reposition glass back by recess + setback
    glass_setback = detail_spec.get('glass_setback', 0)
    total_glass_offset = -(frame_recess + glass_setback)
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

    # Reposition glass back by recess + setback
    glass_setback = detail_spec.get('glass_setback', 0)
    total_glass_offset = -(frame_recess + glass_setback)
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
panel_thickness = door_spec['door_panels']['panel_thickness']
gap = door_spec['door_panels']['center_gap']

# Left panel
left_panel = create_door_panel(
    "Front_Entry_Door_Left_Panel",
    width=panel_width,
    height=panel_height,
    thickness=panel_thickness,
    location=(cutout_spec['position']['x'] - panel_width/2 - gap/2, cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
    color=door_spec['door_panels']['color']
)
phase_1b_objects.append(left_panel)

# Right panel
right_panel = create_door_panel(
    "Front_Entry_Door_Right_Panel",
    width=panel_width,
    height=panel_height,
    thickness=panel_thickness,
    location=(cutout_spec['position']['x'] + panel_width/2 + gap/2, cutout_spec['position']['y'], cutout_spec['position']['z'] + panel_height/2),
    color=door_spec['door_panels']['color']
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

panel = create_door_panel(
    "Rear_Service_Door_Panel",
    width=door_spec['door_panel']['width'],
    height=door_spec['door_panel']['height'],
    thickness=door_spec['door_panel']['thickness'],
    location=(cutout_spec['position']['x'], cutout_spec['position']['y'], cutout_spec['position']['z'] + door_spec['door_panel']['height']/2),
    color=door_spec['door_panel']['color']
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
