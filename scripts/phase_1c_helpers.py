"""
Phase 1C Helper Functions - Interior Geometry
Floor, ceiling, and partition walls
"""

import bpy
import bmesh
from mathutils import Vector


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def get_or_create_material(name, hex_color):
    """Get existing material or create new one with given color."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        rgb = hex_to_rgb(hex_color)
        bsdf.inputs['Base Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    return mat


def create_floor(interior_bounds, z_position=0.01, thickness=0.02, color="#8B7355"):
    """
    Create interior floor plane.

    Args:
        interior_bounds: dict with left_x, right_x, front_y, back_y
        z_position: Z height of floor top surface
        thickness: Floor thickness
        color: Hex color for floor material
    """
    width = interior_bounds['right_x'] - interior_bounds['left_x']
    depth = interior_bounds['back_y'] - interior_bounds['front_y']
    center_x = (interior_bounds['left_x'] + interior_bounds['right_x']) / 2
    center_y = (interior_bounds['front_y'] + interior_bounds['back_y']) / 2

    # Create floor mesh
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(center_x, center_y, z_position - thickness/2)
    )
    floor = bpy.context.active_object
    floor.name = "Interior_Floor"
    floor.scale = (width, depth, thickness)

    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Apply material
    mat = get_or_create_material("Phase1C_Floor", color)
    floor.data.materials.append(mat)

    return floor


def create_ceiling(interior_bounds, z_position=3.58, thickness=0.02, color="#F5F5DC"):
    """
    Create interior ceiling plane.

    Args:
        interior_bounds: dict with left_x, right_x, front_y, back_y
        z_position: Z height of ceiling bottom surface
        thickness: Ceiling thickness
        color: Hex color for ceiling material
    """
    width = interior_bounds['right_x'] - interior_bounds['left_x']
    depth = interior_bounds['back_y'] - interior_bounds['front_y']
    center_x = (interior_bounds['left_x'] + interior_bounds['right_x']) / 2
    center_y = (interior_bounds['front_y'] + interior_bounds['back_y']) / 2

    # Create ceiling mesh
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(center_x, center_y, z_position + thickness/2)
    )
    ceiling = bpy.context.active_object
    ceiling.name = "Interior_Ceiling"
    ceiling.scale = (width, depth, thickness)

    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Apply material
    mat = get_or_create_material("Phase1C_Ceiling", color)
    ceiling.data.materials.append(mat)

    return ceiling


def create_wall_segment(name, start_point, end_point, height, thickness, z_bottom=0.01, color="#D3D3D3"):
    """
    Create a single wall segment between two points.

    Args:
        name: Object name
        start_point: (x, y) tuple for wall start
        end_point: (x, y) tuple for wall end
        height: Wall height
        thickness: Wall thickness
        z_bottom: Bottom Z position
        color: Hex color for wall material
    """
    # Calculate wall length and angle
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    length = (dx**2 + dy**2)**0.5

    if length < 0.01:
        return None

    import math
    angle = math.atan2(dy, dx)

    # Wall center
    center_x = (start_point[0] + end_point[0]) / 2
    center_y = (start_point[1] + end_point[1]) / 2
    center_z = z_bottom + height / 2

    # Create wall mesh
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(center_x, center_y, center_z)
    )
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (length, thickness, height)
    wall.rotation_euler.z = angle

    # Apply transforms
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # Apply material
    mat = get_or_create_material("Phase1C_Interior_Wall", color)
    wall.data.materials.append(mat)

    return wall


def create_wall_with_doorway(name, x_pos, y_start, y_end, height, thickness,
                             doorway_y, doorway_width, doorway_height,
                             z_bottom=0.01, color="#D3D3D3"):
    """
    Create a vertical (Y-running) wall with a doorway cutout.

    Args:
        name: Base object name
        x_pos: X position of wall center
        y_start: Y start position
        y_end: Y end position
        height: Wall height
        thickness: Wall thickness
        doorway_y: Y center of doorway
        doorway_width: Width of doorway opening
        doorway_height: Height of doorway opening
        z_bottom: Bottom Z position
        color: Hex color
    """
    objects = []

    # Calculate doorway bounds
    door_y_min = doorway_y - doorway_width / 2
    door_y_max = doorway_y + doorway_width / 2

    # Segment 1: From y_start to door opening
    if door_y_min > y_start:
        seg1_length = door_y_min - y_start
        seg1_center_y = y_start + seg1_length / 2

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, seg1_center_y, z_bottom + height/2))
        seg1 = bpy.context.active_object
        seg1.name = f"{name}_seg1"
        seg1.scale = (thickness, seg1_length, height)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        mat = get_or_create_material("Phase1C_Interior_Wall", color)
        seg1.data.materials.append(mat)
        objects.append(seg1)

    # Segment 2: Above doorway
    header_height = height - doorway_height
    if header_height > 0.01:
        header_z = z_bottom + doorway_height + header_height / 2

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, doorway_y, header_z))
        header = bpy.context.active_object
        header.name = f"{name}_header"
        header.scale = (thickness, doorway_width, header_height)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        mat = get_or_create_material("Phase1C_Interior_Wall", color)
        header.data.materials.append(mat)
        objects.append(header)

    # Segment 3: From door opening to y_end
    if y_end > door_y_max:
        seg3_length = y_end - door_y_max
        seg3_center_y = door_y_max + seg3_length / 2

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, seg3_center_y, z_bottom + height/2))
        seg3 = bpy.context.active_object
        seg3.name = f"{name}_seg3"
        seg3.scale = (thickness, seg3_length, height)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        mat = get_or_create_material("Phase1C_Interior_Wall", color)
        seg3.data.materials.append(mat)
        objects.append(seg3)

    return objects


def create_horizontal_wall(name, y_pos, x_start, x_end, height, thickness, z_bottom=0.01, color="#D3D3D3"):
    """
    Create a horizontal (X-running) wall segment.

    Args:
        name: Object name
        y_pos: Y position of wall center
        x_start: X start position
        x_end: X end position
        height: Wall height
        thickness: Wall thickness
        z_bottom: Bottom Z position
        color: Hex color
    """
    length = x_end - x_start
    center_x = (x_start + x_end) / 2
    center_z = z_bottom + height / 2

    bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, y_pos, center_z))
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (length, thickness, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    mat = get_or_create_material("Phase1C_Interior_Wall", color)
    wall.data.materials.append(mat)

    return wall


def create_vertical_wall(name, x_pos, y_start, y_end, height, thickness, z_bottom=0.01, color="#D3D3D3"):
    """
    Create a vertical (Y-running) wall segment without doorways.

    Args:
        name: Object name
        x_pos: X position of wall center
        y_start: Y start position
        y_end: Y end position
        height: Wall height
        thickness: Wall thickness
        z_bottom: Bottom Z position
        color: Hex color
    """
    length = y_end - y_start
    center_y = (y_start + y_end) / 2
    center_z = z_bottom + height / 2

    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, center_y, center_z))
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (thickness, length, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    mat = get_or_create_material("Phase1C_Interior_Wall", color)
    wall.data.materials.append(mat)

    return wall


def build_interior_geometry():
    """
    Build all Phase 1C interior geometry.
    Returns list of created objects.
    """
    created_objects = []

    # Interior bounds (from spec)
    interior_bounds = {
        'left_x': -4.07,
        'right_x': 4.07,
        'front_y': -7.32,
        'back_y': 7.32
    }

    # Phase 1C colors
    FLOOR_COLOR = "#8B7355"
    CEILING_COLOR = "#F5F5DC"
    WALL_COLOR = "#D3D3D3"

    # Wall parameters
    WALL_THICKNESS = 0.10
    WALL_HEIGHT = 3.60
    Z_BOTTOM = 0.01
    DOORWAY_WIDTH = 0.9
    DOORWAY_HEIGHT = 2.1

    # Create floor
    floor = create_floor(interior_bounds, z_position=0.01, thickness=0.02, color=FLOOR_COLOR)
    created_objects.append(floor)
    print(f"Created: {floor.name}")

    # Create ceiling
    ceiling = create_ceiling(interior_bounds, z_position=3.58, thickness=0.02, color=CEILING_COLOR)
    created_objects.append(ceiling)
    print(f"Created: {ceiling.name}")

    # Create partition walls

    # 1. Storefront back wall (horizontal wall at y=-1.0, from left edge to hallway)
    storefront_wall = create_horizontal_wall(
        name="Interior_Storefront_BackWall",
        y_pos=-1.0,
        x_start=-4.07,
        x_end=0.0,
        height=WALL_HEIGHT,
        thickness=WALL_THICKNESS,
        z_bottom=Z_BOTTOM,
        color=WALL_COLOR
    )
    created_objects.append(storefront_wall)
    print(f"Created: {storefront_wall.name}")

    # 2. Hallway left wall (vertical wall at x=0.0, from y=-1.0 to back)
    hallway_left_wall = create_vertical_wall(
        name="Interior_Hallway_LeftWall",
        x_pos=0.0,
        y_start=-1.0,
        y_end=7.32,
        height=WALL_HEIGHT,
        thickness=WALL_THICKNESS,
        z_bottom=Z_BOTTOM,
        color=WALL_COLOR
    )
    created_objects.append(hallway_left_wall)
    print(f"Created: {hallway_left_wall.name}")

    # 3. Hallway right wall with two doorways (at x=2.0)
    # Door to Room 2 at y=1.75, Door to Room 1 at y=5.0
    # We need to create segments around the doorways

    # Segment from y=-1.0 to first door (y=1.75 - 0.45 = 1.30)
    seg1 = create_vertical_wall(
        name="Interior_Hallway_RightWall_Seg1",
        x_pos=2.0,
        y_start=-1.0,
        y_end=1.30,  # Door center 1.75 - half width 0.45
        height=WALL_HEIGHT,
        thickness=WALL_THICKNESS,
        z_bottom=Z_BOTTOM,
        color=WALL_COLOR
    )
    created_objects.append(seg1)
    print(f"Created: {seg1.name}")

    # Header above Room 2 door
    header1_height = WALL_HEIGHT - DOORWAY_HEIGHT
    header1 = create_horizontal_wall(
        name="Interior_Room2_Door_Header",
        y_pos=1.75,
        x_start=2.0 - WALL_THICKNESS/2,
        x_end=2.0 + WALL_THICKNESS/2,
        height=header1_height,
        thickness=DOORWAY_WIDTH,
        z_bottom=Z_BOTTOM + DOORWAY_HEIGHT,
        color=WALL_COLOR
    )
    # Fix orientation - this should be a vertical slice
    bpy.data.objects.remove(header1, do_unlink=True)

    # Create header properly
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.0, 1.75, Z_BOTTOM + DOORWAY_HEIGHT + header1_height/2))
    header1 = bpy.context.active_object
    header1.name = "Interior_Room2_Door_Header"
    header1.scale = (WALL_THICKNESS, DOORWAY_WIDTH, header1_height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = get_or_create_material("Phase1C_Interior_Wall", WALL_COLOR)
    header1.data.materials.append(mat)
    created_objects.append(header1)
    print(f"Created: {header1.name}")

    # Segment between doors (y=2.20 to y=4.55)
    seg2 = create_vertical_wall(
        name="Interior_Hallway_RightWall_Seg2",
        x_pos=2.0,
        y_start=2.20,  # Door center 1.75 + half width 0.45
        y_end=4.55,    # Door center 5.0 - half width 0.45
        height=WALL_HEIGHT,
        thickness=WALL_THICKNESS,
        z_bottom=Z_BOTTOM,
        color=WALL_COLOR
    )
    created_objects.append(seg2)
    print(f"Created: {seg2.name}")

    # Header above Room 1 door
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.0, 5.0, Z_BOTTOM + DOORWAY_HEIGHT + header1_height/2))
    header2 = bpy.context.active_object
    header2.name = "Interior_Room1_Door_Header"
    header2.scale = (WALL_THICKNESS, DOORWAY_WIDTH, header1_height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    header2.data.materials.append(mat)
    created_objects.append(header2)
    print(f"Created: {header2.name}")

    # Segment from second door to back wall (y=5.45 to y=7.32)
    seg3 = create_vertical_wall(
        name="Interior_Hallway_RightWall_Seg3",
        x_pos=2.0,
        y_start=5.45,  # Door center 5.0 + half width 0.45
        y_end=7.32,
        height=WALL_HEIGHT,
        thickness=WALL_THICKNESS,
        z_bottom=Z_BOTTOM,
        color=WALL_COLOR
    )
    created_objects.append(seg3)
    print(f"Created: {seg3.name}")

    # 4. Room 1/Room 2 divider (horizontal wall at y=3.5)
    room_divider = create_horizontal_wall(
        name="Interior_Room_Divider",
        y_pos=3.5,
        x_start=2.0,
        x_end=4.07,
        height=WALL_HEIGHT,
        thickness=WALL_THICKNESS,
        z_bottom=Z_BOTTOM,
        color=WALL_COLOR
    )
    created_objects.append(room_divider)
    print(f"Created: {room_divider.name}")

    print(f"\nPhase 1C: Created {len(created_objects)} interior objects")
    return created_objects


def create_interior_collection():
    """Create a collection for Phase 1C interior objects."""
    if "Phase_1C_Interior" not in bpy.data.collections:
        collection = bpy.data.collections.new("Phase_1C_Interior")
        bpy.context.scene.collection.children.link(collection)
    return bpy.data.collections["Phase_1C_Interior"]


def move_to_collection(obj, collection):
    """Move object to specified collection."""
    # Remove from current collections
    for col in obj.users_collection:
        col.objects.unlink(obj)
    # Add to target collection
    collection.objects.link(obj)


if __name__ == "__main__":
    # Test build
    objects = build_interior_geometry()
    print(f"Built {len(objects)} interior objects")
