"""
Phase 1A Iteration Build Template - WITH ENFORCED VERIFICATION GATES

This template provides a structured workflow that makes it mechanically impossible
to skip verification steps.

The template has numbered sections with hard checkpoints that MUST be completed
in order. Export is gated on all verification checkpoints existing.

Usage:
    1. Copy this template for each new iteration
    2. Set the iteration_num variable
    3. Execute sections in order
    4. Each verification section creates a required checkpoint
    5. Export WILL FAIL if any checkpoint is missing

Example:
    iteration_num = 6  # Set this first
    exec(open('scripts/build_template_phase_1a.py').read())
"""

import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent if '__file__' in globals() else Path("C:/Users/brian/Documents/Blender/Creepy Building Myrtle Beach Highway/scripts")
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

import bpy
import yaml
from blender_helpers import (
    create_box,
    create_cylinder,
    verify_dimensions,
    verify_all_objects,
    apply_material,
    create_boolean_cutter
)
from verification_checkpoints import create_checkpoint
from export_with_verification import export_glb_phase_1a

# ============================================================================
# CONFIGURATION
# ============================================================================

# REQUIRED: Set iteration number before running
if 'iteration_num' not in globals():
    raise ValueError(
        "\n" + "="*70 + "\n"
        "ERROR: iteration_num not set\n"
        "="*70 + "\n"
        "You must set the iteration number before running this template:\n\n"
        "    iteration_num = 6  # Set this\n"
        "    exec(open('scripts/build_template_phase_1a.py').read())\n"
        "="*70 + "\n"
    )

print("="*70)
print(f" Phase 1A Iteration {iteration_num:03d} - Build with Enforced Verification")
print("="*70)
print(f"\nThis build process has mandatory verification gates.")
print(f"Export will be BLOCKED if any verification step is incomplete.\n")

# Load specification
spec_path = scripts_dir.parent / 'work' / 'spec' / 'phase_1a' / 'building_geometry.yaml'
with open(spec_path, 'r') as f:
    spec = yaml.safe_load(f)

overall = spec['overall']
walls = spec['walls']
roof = spec['roof']
canopy = spec['canopy']
chimney = spec['chimney']
cutouts = spec['cutouts']

# Extract commonly used dimensions for easier access
building_width = overall['footprint']['width']
building_depth = overall['footprint']['depth']
wall_height = walls['height']

# ============================================================================
# SECTION 1: BUILD GEOMETRY
# ============================================================================
print("\n" + "="*70)
print(" SECTION 1: Building Geometry")
print("="*70)

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Foundation
print("\n[1.1] Building Foundation...")
foundation_height = 0.28
foundation = create_box(
    "Foundation",
    width=building_width,
    depth=building_depth,
    height=foundation_height,
    location=(0, 0, -foundation_height/2)  # Below Z=0 so walls start at Z=0
)
apply_material(foundation, spec.get('phase_1a_colors', {}).get('foundation', '#606060'))

# Walls (start at Z=0, which is top of foundation in spec coordinate system)
print("[1.2] Building Walls...")
wall_base_z = wall_height/2  # Walls start at Z=0

wall_front = create_box(
    "Wall_Front",
    width=building_width,
    depth=walls['thickness'],
    height=wall_height,
    location=(0, -building_depth/2, wall_base_z)
)

wall_rear = create_box(
    "Wall_Rear",
    width=building_width,
    depth=walls['thickness'],
    height=wall_height,
    location=(0, building_depth/2, wall_base_z)
)

wall_left = create_box(
    "Wall_Left",
    width=walls['thickness'],
    depth=building_depth,
    height=wall_height,
    location=(-building_width/2, 0, wall_base_z)
)

wall_right = create_box(
    "Wall_Right",
    width=walls['thickness'],
    depth=building_depth,
    height=wall_height,
    location=(building_width/2, 0, wall_base_z)
)

for wall in [wall_front, wall_rear, wall_left, wall_right]:
    apply_material(wall, spec.get('phase_1a_colors', {}).get('walls', '#808080'))

# Door Alcove Walls (ANGLED - trapezoid shape)
print("[1.2.5] Building Door Alcove Walls...")
door_alcove = spec.get('door_alcove', {})
if door_alcove.get('enabled', False):
    import bmesh

    alcove_wall_thickness = door_alcove['walls']['thickness']
    alcove_height = door_alcove['height']
    y_front = door_alcove['position']['y_front']  # -7.5
    y_back_center = door_alcove['position']['y_back']    # -6.5 (center of back wall)
    # Side walls should stop at front face of back wall to avoid overlap
    y_back = y_back_center - alcove_wall_thickness / 2  # -6.59 (front face of back wall)

    # Left wall: angled from wide front to narrow back
    left_front_x = door_alcove['walls']['left']['front_x']  # -1.55
    left_back_x = door_alcove['walls']['left']['back_x']    # -0.6

    # Create left wall as angled plane
    mesh = bpy.data.meshes.new("Alcove_Wall_Left_Mesh")
    obj = bpy.data.objects.new("Alcove_Wall_Left", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    # Create vertices for angled wall (front outer, front inner, back inner, back outer) at base and top
    # Outer edge (toward building exterior)
    v0 = bm.verts.new((left_front_x - alcove_wall_thickness/2, y_front, 0))  # Front outer base
    v1 = bm.verts.new((left_back_x - alcove_wall_thickness/2, y_back, 0))   # Back outer base
    v2 = bm.verts.new((left_back_x - alcove_wall_thickness/2, y_back, alcove_height))   # Back outer top
    v3 = bm.verts.new((left_front_x - alcove_wall_thickness/2, y_front, alcove_height))  # Front outer top
    # Inner edge (toward alcove interior)
    v4 = bm.verts.new((left_front_x + alcove_wall_thickness/2, y_front, 0))  # Front inner base
    v5 = bm.verts.new((left_back_x + alcove_wall_thickness/2, y_back, 0))   # Back inner base
    v6 = bm.verts.new((left_back_x + alcove_wall_thickness/2, y_back, alcove_height))   # Back inner top
    v7 = bm.verts.new((left_front_x + alcove_wall_thickness/2, y_front, alcove_height))  # Front inner top

    # Create faces
    bm.faces.new([v0, v1, v2, v3])  # Outer face
    bm.faces.new([v4, v7, v6, v5])  # Inner face
    bm.faces.new([v0, v3, v7, v4])  # Front edge
    bm.faces.new([v1, v5, v6, v2])  # Back edge
    bm.faces.new([v3, v2, v6, v7])  # Top edge
    bm.faces.new([v0, v4, v5, v1])  # Bottom edge

    bm.to_mesh(mesh)
    bm.free()
    apply_material(obj, spec.get('phase_1a_colors', {}).get('walls', '#808080'))

    # Right wall: angled from wide front to narrow back (mirror of left)
    right_front_x = door_alcove['walls']['right']['front_x']  # 1.55
    right_back_x = door_alcove['walls']['right']['back_x']    # 0.6

    mesh = bpy.data.meshes.new("Alcove_Wall_Right_Mesh")
    obj = bpy.data.objects.new("Alcove_Wall_Right", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    # Create vertices for angled wall (mirrored)
    v0 = bm.verts.new((right_front_x + alcove_wall_thickness/2, y_front, 0))  # Front outer base
    v1 = bm.verts.new((right_back_x + alcove_wall_thickness/2, y_back, 0))   # Back outer base
    v2 = bm.verts.new((right_back_x + alcove_wall_thickness/2, y_back, alcove_height))   # Back outer top
    v3 = bm.verts.new((right_front_x + alcove_wall_thickness/2, y_front, alcove_height))  # Front outer top
    v4 = bm.verts.new((right_front_x - alcove_wall_thickness/2, y_front, 0))  # Front inner base
    v5 = bm.verts.new((right_back_x - alcove_wall_thickness/2, y_back, 0))   # Back inner base
    v6 = bm.verts.new((right_back_x - alcove_wall_thickness/2, y_back, alcove_height))   # Back inner top
    v7 = bm.verts.new((right_front_x - alcove_wall_thickness/2, y_front, alcove_height))  # Front inner top

    # Create faces
    bm.faces.new([v0, v1, v2, v3])  # Outer face
    bm.faces.new([v4, v7, v6, v5])  # Inner face
    bm.faces.new([v0, v3, v7, v4])  # Front edge
    bm.faces.new([v1, v5, v6, v2])  # Back edge
    bm.faces.new([v3, v2, v6, v7])  # Top edge
    bm.faces.new([v0, v4, v5, v1])  # Bottom edge

    bm.to_mesh(mesh)
    bm.free()
    apply_material(obj, spec.get('phase_1a_colors', {}).get('walls', '#808080'))

    # Back wall of alcove (where door will be)
    if door_alcove['walls'].get('back', {}).get('enabled', False):
        back_wall_width = door_alcove['walls']['back']['width']
        back_wall_height = door_alcove['walls']['back']['height']
        back_wall_y = door_alcove['walls']['back']['position_y']

        alcove_back_wall = create_box(
            "Alcove_Wall_Back",
            width=back_wall_width,
            depth=alcove_wall_thickness,
            height=back_wall_height,
            location=(0, back_wall_y, back_wall_height/2)
        )
        apply_material(alcove_back_wall, spec.get('phase_1a_colors', {}).get('walls', '#808080'))

    # Alcove ceiling (trapezoidal piece covering the top)
    if door_alcove.get('ceiling', {}).get('enabled', False):
        ceiling_spec = door_alcove['ceiling']
        ceiling_thickness = ceiling_spec['thickness']
        ceiling_elevation = ceiling_spec['elevation']
        ceiling_front_width = ceiling_spec['front_width']
        ceiling_back_width = ceiling_spec['back_width']
        ceiling_depth = ceiling_spec['depth']

        # Create trapezoidal mesh for alcove ceiling
        mesh = bpy.data.meshes.new("Alcove_Ceiling_Mesh")
        obj = bpy.data.objects.new("Alcove_Ceiling", mesh)
        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()

        # Trapezoid vertices (bottom face at Z=ceiling_elevation)
        # Front edge (wider)
        front_left_x = -ceiling_front_width / 2
        front_right_x = ceiling_front_width / 2
        front_y = door_alcove['position']['y_front']  # -7.5

        # Back edge (narrower)
        back_left_x = -ceiling_back_width / 2
        back_right_x = ceiling_back_width / 2
        back_y = door_alcove['position']['y_back']  # -6.5

        # Bottom face vertices (at ceiling elevation)
        v0 = bm.verts.new((front_left_x, front_y, ceiling_elevation))
        v1 = bm.verts.new((front_right_x, front_y, ceiling_elevation))
        v2 = bm.verts.new((back_right_x, back_y, ceiling_elevation))
        v3 = bm.verts.new((back_left_x, back_y, ceiling_elevation))

        # Top face vertices (at ceiling_elevation + thickness)
        v4 = bm.verts.new((front_left_x, front_y, ceiling_elevation + ceiling_thickness))
        v5 = bm.verts.new((front_right_x, front_y, ceiling_elevation + ceiling_thickness))
        v6 = bm.verts.new((back_right_x, back_y, ceiling_elevation + ceiling_thickness))
        v7 = bm.verts.new((back_left_x, back_y, ceiling_elevation + ceiling_thickness))

        # Create faces
        bm.faces.new([v0, v1, v2, v3])  # Bottom face
        bm.faces.new([v4, v7, v6, v5])  # Top face
        bm.faces.new([v0, v4, v5, v1])  # Front edge
        bm.faces.new([v2, v6, v7, v3])  # Back edge
        bm.faces.new([v1, v5, v6, v2])  # Right side
        bm.faces.new([v0, v3, v7, v4])  # Left side

        bm.to_mesh(mesh)
        bm.free()
        apply_material(obj, spec.get('phase_1a_colors', {}).get('walls', '#808080'))

        print(f"  ✓ Alcove ceiling created: trapezoidal {ceiling_front_width}m × {ceiling_back_width}m, thickness {ceiling_thickness}m")

    # Alcove header bar (horizontal lintel across top of opening)
    if door_alcove.get('header_bar', {}).get('enabled', False):
        header_spec = door_alcove['header_bar']
        header_width = header_spec['width']
        header_height = header_spec['height']
        header_depth = header_spec['depth']
        header_x = header_spec['position']['x']
        header_y = header_spec['position']['y']
        header_z_top = header_spec['position']['z']

        # Center Z position (top of header is at z_top, so center is z_top - height/2)
        header_z_center = header_z_top - header_height / 2

        header_bar = create_box(
            "Alcove_Header_Bar",
            width=header_width,
            depth=header_depth,
            height=header_height,
            location=(header_x, header_y, header_z_center)
        )
        apply_material(header_bar, spec.get('phase_1a_colors', {}).get('walls', '#808080'))

        print(f"  ✓ Alcove header bar created: {header_width}m wide × {header_height}m high at top of opening")

    print(f"  ✓ Angled alcove walls created: trapezoid shape, front {door_alcove['front_opening']}m → back {door_alcove['back_opening']}m")
else:
    print("  Alcove disabled in spec")

# Roof
print("[1.3] Building Roof...")
roof_z = wall_height + roof['thickness']/2  # Roof sits on walls at Z=wall_height
# Roof extends to outer wall faces (flush with walls)
roof_width = roof.get('width', building_width + walls['thickness'])  # Default: cover walls
roof_depth = roof.get('depth', building_depth + walls['thickness'])
roof_obj = create_box(
    "Roof",
    width=roof_width,
    depth=roof_depth,
    height=roof['thickness'],
    location=(0, 0, roof_z)
)
apply_material(roof_obj, spec.get('phase_1a_colors', {}).get('roof', '#404040'))
print(f"  Roof: {roof_width}m × {roof_depth}m (extends to outer wall faces)")

# Parapet (3-level stepped)
print("[1.3.5] Building Parapet...")
parapet_spec = spec.get('parapet', {})
if parapet_spec.get('enabled', True):  # Default to enabled since it's in baseline
    parapet_config = parapet_spec.get('stepped_configuration', {})
    parapet_thickness = parapet_spec.get('thickness', 0.10)
    roof_top = wall_height + roof['thickness']  # 3.95m (top of roof in spec coordinates)

    # Front facade parapet (flat across front, 3 inches taller than side parapets)
    front_facade_height = parapet_spec.get('front_facade', {}).get('height', 0.53)

    parapet_front = create_box(
        "Parapet_Front",
        width=roof_width,  # Use roof width to cover full roof edge
        depth=parapet_thickness,
        height=front_facade_height,
        location=(0, -building_depth/2, roof_top + front_facade_height/2)
    )
    apply_material(parapet_front, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    # Side parapets - 4 levels with equal height steps (0.45m → 0.30m → 0.15m → 0.0m)
    # Level 1 - Front section (0.45m above roof, spans first 3.75m depth)
    level_1_height = parapet_config.get('level_1_height', 0.45)
    level_1_span = parapet_config.get('level_1_span', 3.75)
    level_1_y_center = -building_depth/2 + level_1_span/2  # -7.5 + 1.875 = -5.625

    parapet_left_level_1 = create_box(
        "Parapet_Left_Level_1",
        width=parapet_thickness,
        depth=level_1_span,
        height=level_1_height,
        location=(-building_width/2, level_1_y_center, roof_top + level_1_height/2)
    )
    apply_material(parapet_left_level_1, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    parapet_right_level_1 = create_box(
        "Parapet_Right_Level_1",
        width=parapet_thickness,
        depth=level_1_span,
        height=level_1_height,
        location=(building_width/2, level_1_y_center, roof_top + level_1_height/2)
    )
    apply_material(parapet_right_level_1, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    # Level 2 - Second section (0.30m above roof, spans next 3.75m depth)
    level_2_height = parapet_config.get('level_2_height', 0.30)
    level_2_span = parapet_config.get('level_2_span', 3.75)
    level_2_y_center = -building_depth/2 + level_1_span + level_2_span/2  # -7.5 + 3.75 + 1.875 = -1.875

    parapet_left_level_2 = create_box(
        "Parapet_Left_Level_2",
        width=parapet_thickness,
        depth=level_2_span,
        height=level_2_height,
        location=(-building_width/2, level_2_y_center, roof_top + level_2_height/2)
    )
    apply_material(parapet_left_level_2, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    parapet_right_level_2 = create_box(
        "Parapet_Right_Level_2",
        width=parapet_thickness,
        depth=level_2_span,
        height=level_2_height,
        location=(building_width/2, level_2_y_center, roof_top + level_2_height/2)
    )
    apply_material(parapet_right_level_2, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    # Level 3 - Third section (0.15m above roof, spans next 3.75m depth)
    level_3_height = parapet_config.get('level_3_height', 0.15)
    level_3_span = parapet_config.get('level_3_span', 3.75)
    level_3_y_center = -building_depth/2 + level_1_span + level_2_span + level_3_span/2  # -7.5 + 3.75 + 3.75 + 1.875 = 1.875

    parapet_left_level_3 = create_box(
        "Parapet_Left_Level_3",
        width=parapet_thickness,
        depth=level_3_span,
        height=level_3_height,
        location=(-building_width/2, level_3_y_center, roof_top + level_3_height/2)
    )
    apply_material(parapet_left_level_3, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    parapet_right_level_3 = create_box(
        "Parapet_Right_Level_3",
        width=parapet_thickness,
        depth=level_3_span,
        height=level_3_height,
        location=(building_width/2, level_3_y_center, roof_top + level_3_height/2)
    )
    apply_material(parapet_right_level_3, spec.get('phase_1a_colors', {}).get('parapet', '#8B4513'))

    # Level 4 - Rear section: no parapet (0.0m height, no geometry created)
    print("  ✓ 4-level stepped parapet complete:")
    print(f"    Front facade: {front_facade_height}m (flat)")
    print(f"    Side level 1: {level_1_height}m, level 2: {level_2_height}m, level 3: {level_3_height}m, level 4: none")
else:
    print("  Parapet disabled in spec")

# Canopy
print("[1.4] Building Canopy...")
canopy_thickness = canopy.get('roof_thickness', canopy.get('thickness', 0.35))
canopy_roof_z = canopy['height'] + canopy_thickness/2
canopy_roof = create_box(
    "Canopy_Roof",
    width=canopy['width'],
    depth=canopy['depth'],
    height=canopy_thickness,
    location=(0, -building_depth/2 - canopy['depth']/2, canopy_roof_z)
)
apply_material(canopy_roof, spec.get('phase_1a_colors', {}).get('canopy', '#A0A0A0'))

# Canopy posts
print("[1.5] Building Canopy Posts...")
for i, post_spec in enumerate(canopy['posts']):
    post = create_cylinder(
        f"Canopy_Post_{i+1}",
        radius=post_spec['diameter']/2,
        height=canopy['height'],
        location=(post_spec['x'], post_spec['y'], canopy['height']/2)
    )
    apply_material(post, spec.get('phase_1a_colors', {}).get('canopy', '#A0A0A0'))

# Chimney
print("[1.6] Building Chimney...")
# Chimney sits ON the roof, so Z position is: roof_top + height_above_roof/2
chimney_height = chimney.get('height_above_roof', 1.5)
chimney_base_z = chimney.get('position_z', chimney.get('base_elevation', 3.95))
chimney_z = chimney_base_z + chimney_height/2

chimney_obj = create_box(
    "Chimney",
    width=chimney['width'],
    depth=chimney['depth'],
    height=chimney_height,
    location=(chimney['position_x'], chimney['position_y'], chimney_z)
)
apply_material(chimney_obj, spec.get('phase_1a_colors', {}).get('chimney', '#8B4513'))

# Gabled roof on top of chimney
gabled_roof_spec = chimney.get('gabled_roof', {})
if gabled_roof_spec.get('enabled', False):
    import bmesh

    gable_height = gabled_roof_spec.get('height', 0.3)
    chimney_width = chimney['width']   # X dimension
    chimney_depth = chimney['depth']   # Y dimension
    chimney_x = chimney['position_x']
    chimney_y = chimney['position_y']
    chimney_top_z = chimney_base_z + chimney_height

    # Create gabled roof mesh
    mesh = bpy.data.meshes.new("Chimney_Gable_Mesh")
    gable_obj = bpy.data.objects.new("Chimney_Gable", mesh)
    bpy.context.collection.objects.link(gable_obj)

    bm = bmesh.new()

    # Ridge runs front-to-back (Y axis)
    # Base corners (at chimney top)
    half_width = chimney_width / 2
    half_depth = chimney_depth / 2

    v0 = bm.verts.new((chimney_x - half_width, chimney_y - half_depth, chimney_top_z))  # Front left
    v1 = bm.verts.new((chimney_x + half_width, chimney_y - half_depth, chimney_top_z))  # Front right
    v2 = bm.verts.new((chimney_x + half_width, chimney_y + half_depth, chimney_top_z))  # Rear right
    v3 = bm.verts.new((chimney_x - half_width, chimney_y + half_depth, chimney_top_z))  # Rear left

    # Ridge vertices (at peak)
    v4 = bm.verts.new((chimney_x, chimney_y - half_depth, chimney_top_z + gable_height))  # Front ridge
    v5 = bm.verts.new((chimney_x, chimney_y + half_depth, chimney_top_z + gable_height))  # Rear ridge

    # Create faces
    bm.faces.new([v0, v1, v2, v3])  # Bottom (base)
    bm.faces.new([v0, v4, v1])      # Front gable triangle
    bm.faces.new([v3, v2, v5])      # Rear gable triangle
    bm.faces.new([v0, v3, v5, v4])  # Left sloped rectangle
    bm.faces.new([v1, v4, v5, v2])  # Right sloped rectangle

    bm.to_mesh(mesh)
    bm.free()

    apply_material(gable_obj, spec.get('phase_1a_colors', {}).get('chimney', '#8B4513'))
    print(f"  ✓ Chimney gabled roof created: {gable_height}m tall")

# Boolean cutouts
print("[1.7] Applying Boolean Cutouts...")
cutout_count = 0

# Wall name mapping: spec uses "front"/"rear"/"left"/"right", objects use "Wall_Front" etc
wall_name_map = {
    'front': 'Wall_Front',
    'rear': 'Wall_Rear',
    'left': 'Wall_Left',
    'right': 'Wall_Right',
    'alcove_left': 'Alcove_Wall_Left',
    'alcove_right': 'Alcove_Wall_Right',
    'alcove_back': 'Alcove_Wall_Back'
}

# Calculate alcove wall angles for rotated cutters
import math
if door_alcove.get('enabled', False):
    alcove_y_front = door_alcove['position']['y_front']  # -7.5
    alcove_y_back = door_alcove['position']['y_back']    # -6.5
    alcove_depth_y = alcove_y_back - alcove_y_front      # 1.0

    # Left wall angle: from front_x to back_x over alcove depth
    left_dx = door_alcove['walls']['left']['back_x'] - door_alcove['walls']['left']['front_x']
    left_wall_direction_angle = math.atan2(left_dx, alcove_depth_y)  # Angle parallel to wall
    # Rotate 90° from wall direction to cut perpendicular (user confirmed this worked initially)
    alcove_left_angle = math.radians(90) - left_wall_direction_angle

    # Right wall angle: mirror of left
    right_dx = door_alcove['walls']['right']['back_x'] - door_alcove['walls']['right']['front_x']
    right_wall_direction_angle = math.atan2(right_dx, alcove_depth_y)  # Angle parallel to wall
    # Rotate 90° from wall direction to cut perpendicular (user confirmed this worked initially)
    alcove_right_angle = math.radians(90) - right_wall_direction_angle

    print(f"  Alcove wall direction angles: left={math.degrees(left_wall_direction_angle):.1f}°, right={math.degrees(right_wall_direction_angle):.1f}°")
    print(f"  Alcove cutter angles (perpendicular): left={math.degrees(alcove_left_angle):.1f}°, right={math.degrees(alcove_right_angle):.1f}°")

# Iterate over dictionary items (not just keys)
for cutout_name, cutout_spec in cutouts.items():
    # Get wall object using mapped name
    wall_key = cutout_spec.get('wall', '')
    wall_obj_name = wall_name_map.get(wall_key)
    wall_obj = bpy.data.objects.get(wall_obj_name) if wall_obj_name else None

    if wall_obj:
        # Extract position from nested structure
        pos = cutout_spec['position']

        # Determine cutter depth and rotation based on wall orientation
        rotation_z = 0  # Default: no rotation

        if wall_key in ['front', 'rear']:
            # Front/rear walls are thin in Y direction
            cutter_depth = walls['thickness'] + cutout_spec.get('recess_depth', 0) + cutout_spec.get('reveal_depth', 0)
        elif wall_key == 'alcove_left':
            # Left alcove wall: angled, rotate cutter to match
            cutter_depth = door_alcove['walls']['thickness'] + cutout_spec.get('reveal_depth', 0)
            rotation_z = alcove_left_angle
        elif wall_key == 'alcove_right':
            # Right alcove wall: angled, rotate cutter to match
            cutter_depth = door_alcove['walls']['thickness'] + cutout_spec.get('reveal_depth', 0)
            rotation_z = alcove_right_angle
        elif wall_key == 'alcove_back':
            # Alcove back wall is thin in Y direction
            cutter_depth = door_alcove['walls']['thickness'] + cutout_spec.get('reveal_depth', 0)
        else:
            # Left/right walls are thin in X direction
            cutter_depth = walls['thickness'] + cutout_spec.get('reveal_depth', 0)

        create_boolean_cutter(
            wall_obj,
            f"{cutout_name}_Cutter",
            cutout_spec['width'],
            cutter_depth,
            cutout_spec['height'],
            (pos['x'], pos['y'], pos['z'] + cutout_spec['height']/2),  # pos['z'] already in spec coordinates (Z=0 at wall base)
            rotation_z=rotation_z
        )
        cutout_count += 1
        if rotation_z != 0:
            print(f"  Applied cutout: {cutout_name} to {wall_obj_name} (rotated {math.degrees(rotation_z):.1f}°)")
        else:
            print(f"  Applied cutout: {cutout_name} to {wall_obj_name}")
    else:
        print(f"  WARNING: Wall '{wall_key}' not found for cutout '{cutout_name}'")

print(f"✓ Geometry complete: {cutout_count} cutouts applied")

# ============================================================================
# SECTION 2: INLINE VERIFICATION (REQUIRED - CHECKPOINT 1)
# ============================================================================
print("\n" + "="*70)
print(" SECTION 2: Inline Verification (REQUIRED)")
print("="*70)
print("Verifying dimensions of each element...\n")

verification_specs = [
    {'object': foundation, 'width': building_width, 'depth': building_depth, 'height': foundation_height},
    {'object': wall_front, 'width': building_width, 'depth': walls['thickness'], 'height': wall_height},
    {'object': wall_rear, 'width': building_width, 'depth': walls['thickness'], 'height': wall_height},
    {'object': wall_left, 'width': walls['thickness'], 'depth': building_depth, 'height': wall_height},
    {'object': wall_right, 'width': walls['thickness'], 'depth': building_depth, 'height': wall_height},
    {'object': roof_obj, 'width': building_width, 'depth': building_depth, 'height': roof['thickness']},
    {'object': canopy_roof, 'width': canopy['width'], 'depth': canopy['depth'], 'height': canopy_thickness},
    {'object': chimney_obj, 'width': chimney['width'], 'depth': chimney['depth'], 'height': chimney_height},
]

# Add parapet verification if parapet was built
if parapet_spec.get('enabled', True):
    verification_specs.extend([
        {'object': parapet_front, 'width': roof_width, 'depth': parapet_thickness, 'height': front_facade_height},
        {'object': parapet_left_level_1, 'width': parapet_thickness, 'depth': level_1_span, 'height': level_1_height},
        {'object': parapet_right_level_1, 'width': parapet_thickness, 'depth': level_1_span, 'height': level_1_height},
        {'object': parapet_left_level_2, 'width': parapet_thickness, 'depth': level_2_span, 'height': level_2_height},
        {'object': parapet_right_level_2, 'width': parapet_thickness, 'depth': level_2_span, 'height': level_2_height},
        {'object': parapet_left_level_3, 'width': parapet_thickness, 'depth': level_3_span, 'height': level_3_height},
        {'object': parapet_right_level_3, 'width': parapet_thickness, 'depth': level_3_span, 'height': level_3_height},
    ])

inline_results = verify_all_objects(verification_specs, tolerance=0.01)

if inline_results['critical_failures']:
    print(f"\n❌ CRITICAL FAILURES: {inline_results['critical_failures']}")
    raise ValueError(
        f"Inline verification failed with {len(inline_results['critical_failures'])} critical failures.\n"
        f"Cannot proceed until geometry is corrected."
    )

if inline_results['major_failures']:
    print(f"\n⚠️  MAJOR ISSUES: {inline_results['major_failures']}")

print(f"\n✓ Inline verification passed: {len(verification_specs)} objects verified")

# CREATE CHECKPOINT 1
create_checkpoint(
    f"inline_verification_{iteration_num:03d}",
    inline_results
)

# ============================================================================
# SECTION 3: BATCH VERIFICATION (REQUIRED - CHECKPOINT 2)
# ============================================================================
print("\n" + "="*70)
print(" SECTION 3: Batch Verification (REQUIRED)")
print("="*70)
print("Re-verifying all objects together...\n")

# Re-run batch verification to ensure nothing changed
batch_results = verify_all_objects(verification_specs, tolerance=0.01)

if batch_results['critical_failures']:
    raise ValueError(
        f"Batch verification failed with {len(batch_results['critical_failures'])} critical failures.\n"
        f"Failed objects: {batch_results['critical_failures']}"
    )

print(f"✓ Batch verification passed")
print(f"  - Critical failures: {len(batch_results['critical_failures'])}")
print(f"  - Major failures: {len(batch_results['major_failures'])}")
print(f"  - All verifications passed: {batch_results['passed']}")

# CREATE CHECKPOINT 2
create_checkpoint(
    f"batch_verification_{iteration_num:03d}",
    batch_results
)

# ============================================================================
# SECTION 4: AUTOMATED VERIFICATION (REQUIRED - CHECKPOINT 3)
# ============================================================================
print("\n" + "="*70)
print(" SECTION 4: Automated Verification Script (REQUIRED)")
print("="*70)
print("Running automated verification against spec targets...\n")

# Run the automated verification script
# This script will create checkpoint 3 if it passes
exec(open(scripts_dir / 'verify_phase_1a.py').read())

print("\n✓ Automated verification complete (checkpoint created if passed)")

# ============================================================================
# SECTION 5: EXPORT (GATED ON ALL VERIFICATIONS)
# ============================================================================
print("\n" + "="*70)
print(" SECTION 5: Exporting GLB (GATED)")
print("="*70)
print("\nAttempting export with verification gates...\n")

# This will FAIL if any checkpoint is missing
# The export function checks for all 3 checkpoints before proceeding
glb_file = export_glb_phase_1a(iteration_num)

print(f"\n✓ Export succeeded: {glb_file}")

# ============================================================================
# SECTION 6: RENDERS & METRICS (ONLY IF EXPORT SUCCEEDED)
# ============================================================================
print("\n" + "="*70)
print(" SECTION 6: Generating Renders and Metrics")
print("="*70)

# TODO: Add render generation code here
# TODO: Add metrics JSON generation code here

print("\n" + "="*70)
print(f" ✅ ITERATION {iteration_num:03d} COMPLETE")
print("="*70)
print("\nAll verification gates passed:")
print("  ✓ Inline verification (checkpoint 1)")
print("  ✓ Batch verification (checkpoint 2)")
print("  ✓ Automated verification (checkpoint 3)")
print("  ✓ GLB export succeeded")
print("\nYou may now present results to the user.")
print("="*70 + "\n")
