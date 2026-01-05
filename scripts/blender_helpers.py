"""
Blender Geometry Helper Library
Phase 1A - Building Construction Helpers

This module provides tested helper functions for creating Blender geometry
with correct dimensions. Prevents scaling math errors.
"""

import bpy


def create_box(name, width, depth, height, location=(0, 0, 0)):
    """
    Create a box (cube primitive) with exact dimensions.

    Args:
        name (str): Object name
        width (float): X dimension in meters
        depth (float): Y dimension in meters
        height (float): Z dimension in meters
        location (tuple): (x, y, z) center position in meters

    Returns:
        bpy.types.Object: Created Blender object

    Example:
        >>> wall = create_box("Wall_Front", 8.5, 0.18, 3.75, (0, -7.5, 1.875))
    """
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name

    # CORRECT scaling for size=1.0 cube: scale=(width, depth, height)
    # size=1.0 creates a cube from -0.5 to +0.5 (total 1.0 unit)
    # So scale directly by the desired dimension
    obj.scale = (width, depth, height)

    # Save location before transform_apply (it resets to origin)
    saved_location = obj.location.copy()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # Restore location after transform_apply
    obj.location = saved_location

    return obj


def create_cylinder(name, radius, height, location=(0, 0, 0)):
    """
    Create a cylinder with exact dimensions.

    Args:
        name (str): Object name
        radius (float): Radius in meters
        height (float): Height (Z dimension) in meters
        location (tuple): (x, y, z) center position in meters

    Returns:
        bpy.types.Object: Created Blender object

    Example:
        >>> post = create_cylinder("Canopy_Post", 0.09, 2.85, (0, -10, 1.425))
    """
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=height,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name

    return obj


def verify_dimensions(obj, expected_width, expected_depth, expected_height, tolerance=0.01):
    """
    Verify object dimensions match expected values within tolerance.

    Args:
        obj (bpy.types.Object): Blender object to verify
        expected_width (float): Expected X dimension in meters
        expected_depth (float): Expected Y dimension in meters
        expected_height (float): Expected Z dimension in meters
        tolerance (float): Absolute tolerance in meters (default 0.01m = 1cm)

    Returns:
        dict: {
            'passed': bool,
            'errors': list of str,
            'actual': {'width': float, 'depth': float, 'height': float},
            'expected': {'width': float, 'depth': float, 'height': float},
            'error_pct': {'width': float, 'depth': float, 'height': float}
        }

    Example:
        >>> result = verify_dimensions(wall, 8.5, 0.18, 3.75)
        >>> if not result['passed']:
        ...     raise ValueError(f"Wall dimensions incorrect: {result['errors']}")
    """
    actual = obj.dimensions
    errors = []
    error_pct = {}

    # Check width (X)
    if expected_width > 0:
        error_pct['width'] = abs(actual.x - expected_width) / expected_width * 100
        if abs(actual.x - expected_width) > tolerance:
            errors.append(
                f"Width (X): expected {expected_width}m, got {actual.x:.3f}m "
                f"({error_pct['width']:.1f}% error)"
            )

    # Check depth (Y)
    if expected_depth > 0:
        error_pct['depth'] = abs(actual.y - expected_depth) / expected_depth * 100
        if abs(actual.y - expected_depth) > tolerance:
            errors.append(
                f"Depth (Y): expected {expected_depth}m, got {actual.y:.3f}m "
                f"({error_pct['depth']:.1f}% error)"
            )

    # Check height (Z)
    if expected_height > 0:
        error_pct['height'] = abs(actual.z - expected_height) / expected_height * 100
        if abs(actual.z - expected_height) > tolerance:
            errors.append(
                f"Height (Z): expected {expected_height}m, got {actual.z:.3f}m "
                f"({error_pct['height']:.1f}% error)"
            )

    return {
        'passed': len(errors) == 0,
        'errors': errors,
        'actual': {
            'width': float(actual.x),
            'depth': float(actual.y),
            'height': float(actual.z)
        },
        'expected': {
            'width': expected_width,
            'depth': expected_depth,
            'height': expected_height
        },
        'error_pct': error_pct
    }


def apply_material(obj, color_hex, material_name=None):
    """
    Apply a simple solid color material to an object.

    Args:
        obj (bpy.types.Object): Blender object
        color_hex (str): Hex color code (e.g., "#808080")
        material_name (str, optional): Material name. If None, uses obj.name + "_mat"

    Returns:
        bpy.types.Material: Created material

    Example:
        >>> apply_material(wall, "#808080", "Wall_Gray")
    """
    if material_name is None:
        material_name = f"{obj.name}_mat"

    # Create material
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True

    # Get principled BSDF node
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        # Convert hex to RGB
        color_hex = color_hex.lstrip('#')
        r = int(color_hex[0:2], 16) / 255.0
        g = int(color_hex[2:4], 16) / 255.0
        b = int(color_hex[4:6], 16) / 255.0

        bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return mat


def create_boolean_cutter(target_obj, cutter_name, width, depth, height, location, rotation_z=0):
    """
    Create a box cutter and apply Boolean difference to target object.

    Args:
        target_obj (bpy.types.Object): Object to cut
        cutter_name (str): Name for cutter object
        width (float): Cutter X dimension in meters
        depth (float): Cutter Y dimension in meters
        height (float): Cutter Z dimension in meters
        location (tuple): (x, y, z) center position in meters
        rotation_z (float): Rotation around Z axis in radians (default 0)

    Returns:
        bpy.types.Object: Cutter object (hidden)

    Example:
        >>> create_boolean_cutter(wall, "Door_Cutter", 1.2, 1.4, 2.1, (0, -7.5, 1.05))
        >>> create_boolean_cutter(wall, "Window_Cutter", 0.5, 0.8, 2.0, (-1, -7, 1), rotation_z=0.42)
    """
    # Create cutter box
    cutter = create_box(cutter_name, width, depth, height, location)
    print(f"  Created cutter '{cutter_name}' at location: {cutter.location}")

    # Apply rotation if specified
    if rotation_z != 0:
        print(f"  Applying rotation {rotation_z:.4f} rad to '{cutter_name}'")
        cutter.rotation_euler[2] = rotation_z
        # Save location before transform_apply (it sometimes resets to origin)
        saved_location = cutter.location.copy()
        print(f"  Saved location before transform_apply: {saved_location}")
        # Apply the rotation transform so it becomes part of the mesh
        bpy.context.view_layer.objects.active = cutter
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        print(f"  Location after transform_apply: {cutter.location}")
        # Restore location after transform_apply
        cutter.location = saved_location
        print(f"  Restored location to: {cutter.location}")

    # Add Boolean modifier to target
    print(f"  Adding boolean modifier to '{target_obj.name}' using '{cutter_name}' at {cutter.location}")
    bool_mod = target_obj.modifiers.new(name=f"Bool_{cutter_name}", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter

    # Apply modifier
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    print(f"  Boolean modifier applied. Cutter final location: {cutter.location}")

    # Hide cutter
    cutter.hide_render = True
    cutter.hide_viewport = True

    return cutter


# Utility function for batch verification
def verify_all_objects(objects_specs, tolerance=0.01):
    """
    Verify dimensions for multiple objects at once.

    Args:
        objects_specs (list): List of dicts with keys:
            - 'object': bpy.types.Object
            - 'width': expected width
            - 'depth': expected depth
            - 'height': expected height
        tolerance (float): Absolute tolerance in meters

    Returns:
        dict: {
            'passed': bool (True if ALL passed),
            'results': dict mapping object names to verification results,
            'critical_failures': list of object names with >10% error,
            'major_failures': list of object names with 5-10% error
        }

    Example:
        >>> specs = [
        ...     {'object': wall_front, 'width': 8.5, 'depth': 0.18, 'height': 3.75},
        ...     {'object': wall_rear, 'width': 8.5, 'depth': 0.18, 'height': 3.75},
        ... ]
        >>> results = verify_all_objects(specs)
        >>> if not results['passed']:
        ...     print(f"Verification failed: {results['critical_failures']}")
    """
    results = {}
    critical_failures = []
    major_failures = []
    all_passed = True

    for spec in objects_specs:
        obj = spec['object']
        result = verify_dimensions(
            obj,
            spec['width'],
            spec['depth'],
            spec['height'],
            tolerance
        )

        results[obj.name] = result

        if not result['passed']:
            all_passed = False

            # Check for critical failures (>10% error in any dimension)
            for dim, err_pct in result['error_pct'].items():
                if err_pct > 10:
                    critical_failures.append(obj.name)
                    break
                elif err_pct > 5:
                    if obj.name not in critical_failures:
                        major_failures.append(obj.name)
                    break

    return {
        'passed': all_passed,
        'results': results,
        'critical_failures': critical_failures,
        'major_failures': major_failures
    }
