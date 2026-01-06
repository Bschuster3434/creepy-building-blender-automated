"""
Blender Helper Library for Phase 1B - Opening Fill
Window frames, glass, and door panels
"""

import bpy


def create_window_frame(name, width, height, thickness, depth, location, rotation_z=0, color="#FFFFFF"):
    """
    Create a window frame (4-sided rectangular frame).

    Args:
        name (str): Frame object name
        width (float): Outer width of frame opening
        height (float): Outer height of frame opening
        thickness (float): Frame profile thickness (e.g., 0.05m)
        depth (float): Frame depth into wall
        location (tuple): (x, y, z) center position
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        list: List of 4 frame pieces [top, bottom, left, right]
    """
    import bmesh
    import bpy
    import math

    frame_pieces = []
    half_w = width / 2
    half_h = height / 2

    # Create pieces at offsets from origin, then rotate around center
    # This ensures all pieces rotate as a group

    # Calculate local offsets (before rotation)
    offsets = {
        'top': (0, 0, half_h - thickness/2),
        'bottom': (0, 0, -half_h + thickness/2),
        'left': (-half_w + thickness/2, 0, 0),
        'right': (half_w - thickness/2, 0, 0)
    }

    # If rotated, calculate world positions after rotation
    if rotation_z != 0:
        cos_r = math.cos(rotation_z)
        sin_r = math.sin(rotation_z)

    pieces_data = [
        ('Top', width, depth, thickness, offsets['top']),
        ('Bottom', width, depth, thickness, offsets['bottom']),
        ('Left', thickness, depth, height - 2*thickness, offsets['left']),
        ('Right', thickness, depth, height - 2*thickness, offsets['right'])
    ]

    for piece_name, w, d, h, offset in pieces_data:
        # Rotate offset around Z axis if needed
        if rotation_z != 0:
            # Rotate the XY components of offset
            rotated_x = offset[0] * cos_r - offset[1] * sin_r
            rotated_y = offset[0] * sin_r + offset[1] * cos_r
            world_loc = (
                location[0] + rotated_x,
                location[1] + rotated_y,
                location[2] + offset[2]
            )
        else:
            world_loc = (
                location[0] + offset[0],
                location[1] + offset[1],
                location[2] + offset[2]
            )

        piece = create_box_helper(
            f"{name}_{piece_name}",
            width=w,
            depth=d,
            height=h,
            location=world_loc
        )

        # Apply rotation around piece's own center
        if rotation_z != 0:
            piece.rotation_euler[2] = rotation_z

        frame_pieces.append(piece)

    # Apply material
    for piece in frame_pieces:
        apply_material_helper(piece, color, f"{name}_Mat")

    return frame_pieces


def create_window_glass(name, width, height, thickness, location, rotation_z=0, color="#000000"):
    """
    Create window glass pane.

    Args:
        name (str): Glass object name
        width (float): Glass width
        height (float): Glass height
        thickness (float): Glass thickness (e.g., 0.01m)
        location (tuple): (x, y, z) center position
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        bpy.types.Object: Glass object
    """
    glass = create_box_helper(
        name,
        width=width,
        depth=thickness,
        height=height,
        location=location
    )

    # Apply rotation if specified
    if rotation_z != 0:
        glass.rotation_euler[2] = rotation_z
        # Don't use transform_apply - just keep rotation in euler

    apply_material_helper(glass, color, f"{name}_Mat")

    return glass


def create_door_frame(name, width, height, thickness, depth, location, rotation_z=0, color="#8B4513"):
    """
    Create a door frame (3-sided: top and sides, no bottom piece).

    Args:
        name (str): Frame object name
        width (float): Outer width of frame opening
        height (float): Outer height of frame opening
        thickness (float): Frame profile thickness
        depth (float): Frame depth into wall
        location (tuple): (x, y, z) center position (at ground level z=height/2)
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        list: List of 3 frame pieces [top, left, right]
    """
    import math

    frame_pieces = []
    half_w = width / 2
    half_h = height / 2

    # Calculate local offsets (before rotation)
    offsets = {
        'top': (0, 0, half_h - thickness/2),
        'left': (-half_w + thickness/2, 0, 0),
        'right': (half_w - thickness/2, 0, 0)
    }

    # If rotated, calculate world positions after rotation
    if rotation_z != 0:
        cos_r = math.cos(rotation_z)
        sin_r = math.sin(rotation_z)

    pieces_data = [
        ('Top', width, depth, thickness, offsets['top']),
        ('Left', thickness, depth, height, offsets['left']),
        ('Right', thickness, depth, height, offsets['right'])
    ]

    for piece_name, w, d, h, offset in pieces_data:
        # Rotate offset around Z axis if needed
        if rotation_z != 0:
            rotated_x = offset[0] * cos_r - offset[1] * sin_r
            rotated_y = offset[0] * sin_r + offset[1] * cos_r
            world_loc = (
                location[0] + rotated_x,
                location[1] + rotated_y,
                location[2] + offset[2]
            )
        else:
            world_loc = (
                location[0] + offset[0],
                location[1] + offset[1],
                location[2] + offset[2]
            )

        piece = create_box_helper(
            f"{name}_{piece_name}",
            width=w,
            depth=d,
            height=h,
            location=world_loc
        )

        # Apply rotation around piece's own center
        if rotation_z != 0:
            piece.rotation_euler[2] = rotation_z

        frame_pieces.append(piece)

    # Apply material
    for piece in frame_pieces:
        apply_material_helper(piece, color, f"{name}_Mat")

    return frame_pieces


def create_door_panel(name, width, height, thickness, location, color="#1A1A1A"):
    """
    Create a door panel (solid rectangular panel).

    Args:
        name (str): Panel object name
        width (float): Panel width
        height (float): Panel height
        thickness (float): Panel thickness
        location (tuple): (x, y, z) center position
        color (str): Hex color code

    Returns:
        bpy.types.Object: Door panel object
    """
    panel = create_box_helper(
        name,
        width=width,
        depth=thickness,
        height=height,
        location=location
    )

    apply_material_helper(panel, color, f"{name}_Mat")

    return panel


def create_outer_trim(name, cutout_width, cutout_height, trim_width_sides, trim_width_top, trim_width_bottom, trim_depth,
                     center_location, rotation_z=0, color="#FFFFFF"):
    """
    Create outer trim around brick opening with different widths for each side.

    Args:
        name (str): Trim object base name
        cutout_width (float): Width of brick cutout opening
        cutout_height (float): Height of brick cutout opening
        trim_width_sides (float): Width of left/right side trim (e.g., 0.08m)
        trim_width_top (float): Width of top trim (e.g., 0.12m)
        trim_width_bottom (float): Width of bottom trim (e.g., 0.12m)
        trim_depth (float): Depth of trim (projection from brick)
        center_location (tuple): (x, y, z) center position of opening
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        list: List of 4 trim pieces [top, bottom, left, right]
    """
    import math

    trim_pieces = []
    half_w = cutout_width / 2
    half_h = cutout_height / 2

    # Calculate local offsets (before rotation)
    offsets = {
        'top': (0, 0, half_h + trim_width_top/2),
        'bottom': (0, 0, -half_h - trim_width_bottom/2),
        'left': (-half_w - trim_width_sides/2, 0, 0),
        'right': (half_w + trim_width_sides/2, 0, 0)
    }

    # If rotated, calculate world positions after rotation
    if rotation_z != 0:
        cos_r = math.cos(rotation_z)
        sin_r = math.sin(rotation_z)

    pieces_data = [
        ('Top', cutout_width + 2*trim_width_sides, trim_depth, trim_width_top, offsets['top']),
        ('Bottom', cutout_width + 2*trim_width_sides, trim_depth, trim_width_bottom, offsets['bottom']),
        ('Left', trim_width_sides, trim_depth, cutout_height, offsets['left']),
        ('Right', trim_width_sides, trim_depth, cutout_height, offsets['right'])
    ]

    for piece_name, w, d, h, offset in pieces_data:
        # Rotate offset around Z axis if needed
        if rotation_z != 0:
            rotated_x = offset[0] * cos_r - offset[1] * sin_r
            rotated_y = offset[0] * sin_r + offset[1] * cos_r
            world_loc = (
                center_location[0] + rotated_x,
                center_location[1] + rotated_y,
                center_location[2] + offset[2]
            )
        else:
            world_loc = (
                center_location[0] + offset[0],
                center_location[1] + offset[1],
                center_location[2] + offset[2]
            )

        piece = create_box_helper(
            f"{name}_OuterTrim_{piece_name}",
            width=w,
            depth=d,
            height=h,
            location=world_loc
        )

        # Apply rotation around piece's own center
        if rotation_z != 0:
            piece.rotation_euler[2] = rotation_z

        trim_pieces.append(piece)

    # Apply material
    for piece in trim_pieces:
        apply_material_helper(piece, color, f"{name}_Trim_Mat")

    return trim_pieces


def create_window_sill(name, width, depth, height, center_location,
                      rotation_z=0, color="#FFFFFF"):
    """
    Create window sill at bottom of window.

    Args:
        name (str): Sill object name
        width (float): Sill width (cutout width + 2×overhang)
        depth (float): Sill depth (projects forward from wall)
        height (float): Sill thickness/height (e.g., 0.03m)
        center_location (tuple): (x, y, z) center position
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        bpy.types.Object: Sill object
    """
    sill = create_box_helper(
        name,
        width=width,
        depth=depth,
        height=height,
        location=center_location
    )

    # Apply rotation if specified
    if rotation_z != 0:
        sill.rotation_euler[2] = rotation_z

    apply_material_helper(sill, color, f"{name}_Mat")

    return sill


def create_door_threshold(name, width, depth, height, center_location,
                         rotation_z=0, color="#8B4513"):
    """
    Create door threshold at bottom of door frame.

    Args:
        name (str): Threshold object name
        width (float): Threshold width (matches door width)
        depth (float): Threshold depth
        height (float): Threshold height (e.g., 0.02m)
        center_location (tuple): (x, y, z) center position
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        bpy.types.Object: Threshold object
    """
    threshold = create_box_helper(
        name,
        width=width,
        depth=depth,
        height=height,
        location=center_location
    )

    # Apply rotation if specified
    if rotation_z != 0:
        threshold.rotation_euler[2] = rotation_z

    apply_material_helper(threshold, color, f"{name}_Mat")

    return threshold


def reposition_frame_pieces(frame_pieces, y_offset):
    """
    Move existing frame pieces back/forward by y_offset.

    Creates reveal between outer trim and window/door frame.

    Args:
        frame_pieces (list): List of frame piece objects
        y_offset (float): Distance to move in Y direction (negative = into wall)
    """
    for piece in frame_pieces:
        piece.location.y += y_offset


def reposition_glass_or_panel(objects, y_offset):
    """
    Move glass or door panels back by y_offset.

    Args:
        objects (list or bpy.types.Object): Glass/panel object(s)
        y_offset (float): Distance to move in Y direction (negative = into wall)
    """
    # Handle both single object and list
    if not isinstance(objects, list):
        objects = [objects]

    for obj in objects:
        obj.location.y += y_offset


# Helper functions (wrappers around blender_helpers.py functions)
def create_box_helper(name, width, depth, height, location):
    """Create box using blender_helpers.create_box"""
    from blender_helpers import create_box
    return create_box(name, width, depth, height, location)


def apply_material_helper(obj, color_hex, material_name=None):
    """Apply material using blender_helpers.apply_material"""
    from blender_helpers import apply_material
    return apply_material(obj, color_hex, material_name)
