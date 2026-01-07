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


def create_horizontal_muntin(name, width, thickness, depth, location, rotation_z=0, color="#FFFFFF"):
    """
    Create a horizontal muntin (divider bar) for a window.

    Args:
        name (str): Muntin object name
        width (float): Width of the muntin (matches glass width)
        thickness (float): Thickness/height of the muntin bar
        depth (float): Depth of the muntin
        location (tuple): (x, y, z) center position
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        bpy.types.Object: Muntin object
    """
    muntin = create_box_helper(
        name,
        width=width,
        depth=depth,
        height=thickness,
        location=location
    )

    if rotation_z != 0:
        muntin.rotation_euler[2] = rotation_z

    apply_material_helper(muntin, color, f"{name}_Mat")

    return muntin


def create_inner_window_frame(name, outer_width, outer_height, outer_frame_thickness,
                              inner_frame_thickness, inner_frame_depth, location,
                              rotation_z=0, color="#FFFFFF"):
    """
    Create an inner window frame (window stop) that sits inside the outer frame.
    This creates the layered/stepped profile visible in traditional windows.

    Args:
        name (str): Frame object name
        outer_width (float): Width of outer frame opening
        outer_height (float): Height of outer frame opening
        outer_frame_thickness (float): Thickness of the outer frame (to calculate inner dimensions)
        inner_frame_thickness (float): Thickness of this inner frame profile (e.g., 0.03m)
        inner_frame_depth (float): Depth of inner frame (e.g., 0.05m)
        location (tuple): (x, y, z) center position
        rotation_z (float): Rotation around Z axis in radians
        color (str): Hex color code

    Returns:
        list: List of 4 inner frame pieces [top, bottom, left, right]
    """
    import math

    # Inner frame sits inside outer frame
    # Inner frame outer dimensions = outer frame inner dimensions
    inner_outer_width = outer_width - 2 * outer_frame_thickness
    inner_outer_height = outer_height - 2 * outer_frame_thickness

    frame_pieces = []
    half_w = inner_outer_width / 2
    half_h = inner_outer_height / 2

    # Calculate local offsets (before rotation)
    offsets = {
        'top': (0, 0, half_h - inner_frame_thickness/2),
        'bottom': (0, 0, -half_h + inner_frame_thickness/2),
        'left': (-half_w + inner_frame_thickness/2, 0, 0),
        'right': (half_w - inner_frame_thickness/2, 0, 0)
    }

    # If rotated, calculate world positions after rotation
    if rotation_z != 0:
        cos_r = math.cos(rotation_z)
        sin_r = math.sin(rotation_z)

    pieces_data = [
        ('Top', inner_outer_width, inner_frame_depth, inner_frame_thickness, offsets['top']),
        ('Bottom', inner_outer_width, inner_frame_depth, inner_frame_thickness, offsets['bottom']),
        ('Left', inner_frame_thickness, inner_frame_depth, inner_outer_height - 2*inner_frame_thickness, offsets['left']),
        ('Right', inner_frame_thickness, inner_frame_depth, inner_outer_height - 2*inner_frame_thickness, offsets['right'])
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
            f"{name}_Inner_{piece_name}",
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
        apply_material_helper(piece, color, f"{name}_Inner_Mat")

    return frame_pieces


def create_french_door_panel(name, width, height, location, stile_width=0.05, rail_width=0.08,
                             muntin_width=0.03, glass_thickness=0.01, panel_depth=0.04,
                             rows=5, cols=2, frame_color="#FFFFFF", glass_color="#000000"):
    """
    Create a French door panel with grid of glass panes (10-lite style).

    Args:
        name (str): Panel object name
        width (float): Total panel width
        height (float): Total panel height
        location (tuple): (x, y, z) center position
        stile_width (float): Width of left/right vertical stiles
        rail_width (float): Height of top/bottom rails
        muntin_width (float): Width/height of muntin bars
        glass_thickness (float): Glass pane thickness
        panel_depth (float): Depth of frame/muntins
        rows (int): Number of glass rows (default 5)
        cols (int): Number of glass columns (default 2)
        frame_color (str): Hex color for frame/muntins
        glass_color (str): Hex color for glass

    Returns:
        dict: Dictionary with 'frame', 'muntins', 'glass' keys containing lists of objects
    """
    import math

    result = {'frame': [], 'muntins': [], 'glass': []}

    half_w = width / 2
    half_h = height / 2

    # --- Create outer stiles and rails ---

    # Left stile
    left_stile = create_box_helper(
        f"{name}_Stile_Left",
        width=stile_width,
        depth=panel_depth,
        height=height,
        location=(location[0] - half_w + stile_width/2, location[1], location[2])
    )
    apply_material_helper(left_stile, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(left_stile)

    # Right stile
    right_stile = create_box_helper(
        f"{name}_Stile_Right",
        width=stile_width,
        depth=panel_depth,
        height=height,
        location=(location[0] + half_w - stile_width/2, location[1], location[2])
    )
    apply_material_helper(right_stile, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(right_stile)

    # Top rail
    top_rail = create_box_helper(
        f"{name}_Rail_Top",
        width=width - 2*stile_width,
        depth=panel_depth,
        height=rail_width,
        location=(location[0], location[1], location[2] + half_h - rail_width/2)
    )
    apply_material_helper(top_rail, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(top_rail)

    # Bottom rail (typically thicker)
    bottom_rail = create_box_helper(
        f"{name}_Rail_Bottom",
        width=width - 2*stile_width,
        depth=panel_depth,
        height=rail_width,
        location=(location[0], location[1], location[2] - half_h + rail_width/2)
    )
    apply_material_helper(bottom_rail, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(bottom_rail)

    # --- Calculate glass area ---
    glass_area_width = width - 2*stile_width
    glass_area_height = height - 2*rail_width
    glass_area_center_z = location[2]

    # --- Create muntins ---
    # Vertical muntins: cols-1 muntins
    vertical_muntins_count = cols - 1
    if vertical_muntins_count > 0:
        glass_col_width = (glass_area_width - vertical_muntins_count * muntin_width) / cols
        for i in range(vertical_muntins_count):
            x_pos = location[0] - glass_area_width/2 + (i+1) * glass_col_width + i * muntin_width + muntin_width/2
            v_muntin = create_box_helper(
                f"{name}_VMuntin_{i+1}",
                width=muntin_width,
                depth=panel_depth,
                height=glass_area_height,
                location=(x_pos, location[1], glass_area_center_z)
            )
            apply_material_helper(v_muntin, frame_color, f"{name}_Muntin_Mat")
            result['muntins'].append(v_muntin)
    else:
        glass_col_width = glass_area_width

    # Horizontal muntins: rows-1 muntins
    horizontal_muntins_count = rows - 1
    if horizontal_muntins_count > 0:
        glass_row_height = (glass_area_height - horizontal_muntins_count * muntin_width) / rows
        for i in range(horizontal_muntins_count):
            z_pos = glass_area_center_z + glass_area_height/2 - (i+1) * glass_row_height - i * muntin_width - muntin_width/2
            h_muntin = create_box_helper(
                f"{name}_HMuntin_{i+1}",
                width=glass_area_width,
                depth=panel_depth,
                height=muntin_width,
                location=(location[0], location[1], z_pos)
            )
            apply_material_helper(h_muntin, frame_color, f"{name}_Muntin_Mat")
            result['muntins'].append(h_muntin)
    else:
        glass_row_height = glass_area_height

    # --- Create glass panes ---
    # Recalculate dimensions based on muntins
    glass_col_width = (glass_area_width - vertical_muntins_count * muntin_width) / cols
    glass_row_height = (glass_area_height - horizontal_muntins_count * muntin_width) / rows

    pane_num = 1
    for row in range(rows):
        for col in range(cols):
            # Calculate pane center position
            x_pos = location[0] - glass_area_width/2 + col * (glass_col_width + muntin_width) + glass_col_width/2
            z_pos = glass_area_center_z + glass_area_height/2 - row * (glass_row_height + muntin_width) - glass_row_height/2

            glass_pane = create_box_helper(
                f"{name}_Glass_{pane_num}",
                width=glass_col_width,
                depth=glass_thickness,
                height=glass_row_height,
                location=(x_pos, location[1], z_pos)
            )
            apply_material_helper(glass_pane, glass_color, f"{name}_Glass_Mat")
            result['glass'].append(glass_pane)
            pane_num += 1

    return result


def create_half_lite_door_panel(name, width, height, location, glass_ratio=0.5,
                                 stile_width=0.05, rail_width=0.08, mid_rail_width=0.10,
                                 muntin_width=0.03, glass_thickness=0.01, panel_depth=0.04,
                                 rows=3, cols=3, panel_inset=0.02,
                                 frame_color="#FFFFFF", glass_color="#000000", panel_color="#FFFFFF"):
    """
    Create a half-lite door panel with upper glass grid and lower raised panels.

    Args:
        name (str): Panel object name
        width (float): Total panel width
        height (float): Total panel height
        location (tuple): (x, y, z) center position
        glass_ratio (float): Ratio of height for glass section (0.5 = half)
        stile_width (float): Width of left/right vertical stiles
        rail_width (float): Height of top/bottom rails
        mid_rail_width (float): Height of rail between glass and panel sections
        muntin_width (float): Width/height of muntin bars in glass section
        glass_thickness (float): Glass pane thickness
        panel_depth (float): Depth of frame/muntins
        rows (int): Number of glass rows
        cols (int): Number of glass columns
        panel_inset (float): Inset depth for raised panels
        frame_color (str): Hex color for frame/muntins
        glass_color (str): Hex color for glass
        panel_color (str): Hex color for raised panels

    Returns:
        dict: Dictionary with 'frame', 'muntins', 'glass', 'panels' keys
    """
    result = {'frame': [], 'muntins': [], 'glass': [], 'panels': []}

    half_w = width / 2
    half_h = height / 2

    # Calculate section heights
    glass_section_height = (height - rail_width * 2 - mid_rail_width) * glass_ratio
    panel_section_height = (height - rail_width * 2 - mid_rail_width) * (1 - glass_ratio)

    # --- Create outer stiles and rails ---

    # Left stile (full height)
    left_stile = create_box_helper(
        f"{name}_Stile_Left",
        width=stile_width,
        depth=panel_depth,
        height=height,
        location=(location[0] - half_w + stile_width/2, location[1], location[2])
    )
    apply_material_helper(left_stile, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(left_stile)

    # Right stile (full height)
    right_stile = create_box_helper(
        f"{name}_Stile_Right",
        width=stile_width,
        depth=panel_depth,
        height=height,
        location=(location[0] + half_w - stile_width/2, location[1], location[2])
    )
    apply_material_helper(right_stile, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(right_stile)

    # Top rail
    inner_width = width - 2*stile_width
    top_rail = create_box_helper(
        f"{name}_Rail_Top",
        width=inner_width,
        depth=panel_depth,
        height=rail_width,
        location=(location[0], location[1], location[2] + half_h - rail_width/2)
    )
    apply_material_helper(top_rail, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(top_rail)

    # Bottom rail
    bottom_rail = create_box_helper(
        f"{name}_Rail_Bottom",
        width=inner_width,
        depth=panel_depth,
        height=rail_width,
        location=(location[0], location[1], location[2] - half_h + rail_width/2)
    )
    apply_material_helper(bottom_rail, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(bottom_rail)

    # Mid rail (between glass and panel sections)
    mid_rail_z = location[2] + half_h - rail_width - glass_section_height - mid_rail_width/2
    mid_rail = create_box_helper(
        f"{name}_Rail_Mid",
        width=inner_width,
        depth=panel_depth,
        height=mid_rail_width,
        location=(location[0], location[1], mid_rail_z)
    )
    apply_material_helper(mid_rail, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(mid_rail)

    # --- Glass section (upper) ---
    glass_area_width = inner_width
    glass_area_height = glass_section_height
    glass_center_z = location[2] + half_h - rail_width - glass_section_height/2

    # Vertical muntins
    vertical_muntins_count = cols - 1
    if vertical_muntins_count > 0:
        glass_col_width = (glass_area_width - vertical_muntins_count * muntin_width) / cols
        for i in range(vertical_muntins_count):
            x_pos = location[0] - glass_area_width/2 + (i+1) * glass_col_width + i * muntin_width + muntin_width/2
            v_muntin = create_box_helper(
                f"{name}_VMuntin_{i+1}",
                width=muntin_width,
                depth=panel_depth,
                height=glass_area_height,
                location=(x_pos, location[1], glass_center_z)
            )
            apply_material_helper(v_muntin, frame_color, f"{name}_Muntin_Mat")
            result['muntins'].append(v_muntin)
    else:
        glass_col_width = glass_area_width

    # Horizontal muntins
    horizontal_muntins_count = rows - 1
    if horizontal_muntins_count > 0:
        glass_row_height = (glass_area_height - horizontal_muntins_count * muntin_width) / rows
        for i in range(horizontal_muntins_count):
            z_pos = glass_center_z + glass_area_height/2 - (i+1) * glass_row_height - i * muntin_width - muntin_width/2
            h_muntin = create_box_helper(
                f"{name}_HMuntin_{i+1}",
                width=glass_area_width,
                depth=panel_depth,
                height=muntin_width,
                location=(location[0], location[1], z_pos)
            )
            apply_material_helper(h_muntin, frame_color, f"{name}_Muntin_Mat")
            result['muntins'].append(h_muntin)
    else:
        glass_row_height = glass_area_height

    # Glass panes
    glass_col_width = (glass_area_width - vertical_muntins_count * muntin_width) / cols
    glass_row_height = (glass_area_height - horizontal_muntins_count * muntin_width) / rows

    pane_num = 1
    for row in range(rows):
        for col in range(cols):
            x_pos = location[0] - glass_area_width/2 + col * (glass_col_width + muntin_width) + glass_col_width/2
            z_pos = glass_center_z + glass_area_height/2 - row * (glass_row_height + muntin_width) - glass_row_height/2

            glass_pane = create_box_helper(
                f"{name}_Glass_{pane_num}",
                width=glass_col_width,
                depth=glass_thickness,
                height=glass_row_height,
                location=(x_pos, location[1], z_pos)
            )
            apply_material_helper(glass_pane, glass_color, f"{name}_Glass_Mat")
            result['glass'].append(glass_pane)
            pane_num += 1

    # --- Panel section (lower) with 2 raised panels ---
    panel_area_height = panel_section_height
    panel_center_z = location[2] - half_h + rail_width + panel_area_height/2

    # Center stile between panels
    center_stile = create_box_helper(
        f"{name}_Stile_Center",
        width=stile_width,
        depth=panel_depth,
        height=panel_area_height,
        location=(location[0], location[1], panel_center_z)
    )
    apply_material_helper(center_stile, frame_color, f"{name}_Frame_Mat")
    result['frame'].append(center_stile)

    # Left raised panel
    panel_width = (inner_width - stile_width) / 2
    left_panel = create_box_helper(
        f"{name}_Panel_Left",
        width=panel_width - 0.02,  # Small gap
        depth=panel_depth - panel_inset,
        height=panel_area_height - 0.02,
        location=(location[0] - panel_width/2 - stile_width/4, location[1] + panel_inset/2, panel_center_z)
    )
    apply_material_helper(left_panel, panel_color, f"{name}_Panel_Mat")
    result['panels'].append(left_panel)

    # Right raised panel
    right_panel = create_box_helper(
        f"{name}_Panel_Right",
        width=panel_width - 0.02,  # Small gap
        depth=panel_depth - panel_inset,
        height=panel_area_height - 0.02,
        location=(location[0] + panel_width/2 + stile_width/4, location[1] + panel_inset/2, panel_center_z)
    )
    apply_material_helper(right_panel, panel_color, f"{name}_Panel_Mat")
    result['panels'].append(right_panel)

    return result


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
