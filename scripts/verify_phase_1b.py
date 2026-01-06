"""
Phase 1B Verification Script

Verifies that window frames and door frames EXACTLY fill Phase 1A cutouts with NO GAPS.

For each opening:
1. Position camera to frame the opening
2. Capture screenshot
3. Measure frame dimensions vs cutout dimensions
4. Verify NO gaps exist

Usage:
    iteration_num = 2
    exec(open('scripts/verify_phase_1b.py').read())
"""

import bpy
import yaml
import sys
import math
from pathlib import Path
from mathutils import Vector

# Add scripts to path
scripts_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd() / 'scripts'
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

from verification_checkpoints import create_checkpoint


def setup_camera_for_opening(opening_name, position, size, normal_direction):
    """
    Position camera to frame a specific opening.

    Args:
        opening_name (str): Name of opening
        position (Vector): Center position of opening
        size (tuple): (width, height) of opening
        normal_direction (Vector): Normal direction facing away from wall

    Returns:
        bpy.types.Object: Camera object
    """
    # Create or get camera
    if "VerificationCamera" in bpy.data.objects:
        camera = bpy.data.objects["VerificationCamera"]
    else:
        camera_data = bpy.data.cameras.new("VerificationCamera")
        camera = bpy.data.objects.new("VerificationCamera", camera_data)
        bpy.context.scene.collection.objects.link(camera)

    # Set camera as active
    bpy.context.scene.camera = camera

    # Position camera to frame the opening
    # Camera should be far enough back to see the entire opening plus some margin
    max_dim = max(size[0], size[1])
    distance = max_dim * 2.5  # Camera distance for good framing

    # Position camera along normal direction
    camera.location = position + (normal_direction * distance)

    # Point camera at opening center
    direction = position - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

    return camera


def capture_opening_screenshot(opening_name, output_dir):
    """
    Capture screenshot of current camera view.

    Args:
        opening_name (str): Name for screenshot file
        output_dir (Path): Output directory

    Returns:
        Path: Screenshot file path
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / f"{opening_name}.png"

    # Set render settings
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = str(screenshot_path)

    # Render
    bpy.ops.render.render(write_still=True)

    return screenshot_path


def verify_opening_fill(opening_name, cutout_spec, phase_1b_spec):
    """
    Verify that frame exactly fills cutout with no gaps.

    Args:
        opening_name (str): Name of opening
        cutout_spec (dict): Phase 1A cutout specification
        phase_1b_spec (dict): Phase 1B frame specification

    Returns:
        dict: Verification result
    """
    result = {
        'opening': opening_name,
        'passed': True,
        'errors': [],
        'warnings': []
    }

    # Get cutout dimensions
    cutout_width = cutout_spec['width']
    cutout_height = cutout_spec['height']

    # Get frame dimensions
    frame_width = phase_1b_spec['frame']['width']
    frame_height = phase_1b_spec['frame']['height']

    # Check if frame exactly matches cutout
    tolerance = 0.001  # 1mm tolerance

    width_diff = abs(frame_width - cutout_width)
    height_diff = abs(frame_height - cutout_height)

    if width_diff > tolerance:
        result['passed'] = False
        result['errors'].append(
            f"Frame width ({frame_width}m) does NOT match cutout width ({cutout_width}m). "
            f"Gap: {width_diff*1000:.1f}mm"
        )

    if height_diff > tolerance:
        result['passed'] = False
        result['errors'].append(
            f"Frame height ({frame_height}m) does NOT match cutout height ({cutout_height}m). "
            f"Gap: {height_diff*1000:.1f}mm"
        )

    # Check if frame position matches cutout position
    cutout_pos = cutout_spec['position']

    # Find frame object in scene
    frame_objects = [obj for obj in bpy.data.objects if opening_name.replace('_', ' ').title().replace(' ', '_') in obj.name and 'Frame' in obj.name]

    if frame_objects:
        # Get bounding box center of all frame pieces
        all_verts = []
        for frame_obj in frame_objects:
            if frame_obj.type == 'MESH':
                for v in frame_obj.data.vertices:
                    world_co = frame_obj.matrix_world @ v.co
                    all_verts.append(world_co)

        if all_verts:
            # Calculate center
            center_x = sum(v.x for v in all_verts) / len(all_verts)
            center_y = sum(v.y for v in all_verts) / len(all_verts)
            center_z = sum(v.z for v in all_verts) / len(all_verts)

            # Expected center (cutout position is at bottom, so add half height)
            expected_z = cutout_pos['z'] + cutout_height / 2

            # Check position
            position_tolerance = 0.01  # 1cm tolerance

            if abs(center_x - cutout_pos['x']) > position_tolerance:
                result['warnings'].append(
                    f"Frame X position ({center_x:.3f}m) may not match cutout X ({cutout_pos['x']:.3f}m)"
                )

            if abs(center_y - cutout_pos['y']) > position_tolerance:
                result['warnings'].append(
                    f"Frame Y position ({center_y:.3f}m) may not match cutout Y ({cutout_pos['y']:.3f}m)"
                )

            if abs(center_z - expected_z) > position_tolerance:
                result['warnings'].append(
                    f"Frame Z center ({center_z:.3f}m) may not match expected Z ({expected_z:.3f}m)"
                )

    return result


def verify_glass_panel_fill(opening_name, phase_1b_spec):
    """
    Verify that glass/panels EXACTLY fill frame inner opening with NO GAPS.

    Args:
        opening_name (str): Name of opening
        phase_1b_spec (dict): Phase 1B specification

    Returns:
        dict: Verification result
    """
    result = {
        'opening': opening_name,
        'passed': True,
        'errors': [],
        'warnings': []
    }

    frame = phase_1b_spec['frame']
    frame_outer_w = frame['width']
    frame_outer_h = frame['height']
    frame_thickness = frame['thickness']

    # Calculate frame INNER opening
    frame_inner_w = frame_outer_w - 2 * frame_thickness

    # CRITICAL: Windows are 4-sided (subtract top AND bottom)
    # Doors are 3-sided (subtract only top, NO bottom piece)
    is_door = 'door_panel' in phase_1b_spec or 'door_panels' in phase_1b_spec
    if is_door:
        # Door frames: 3-sided (left, right, top only)
        frame_inner_h = frame_outer_h - frame_thickness  # Only subtract top
    else:
        # Window frames: 4-sided (left, right, top, bottom)
        frame_inner_h = frame_outer_h - 2 * frame_thickness  # Subtract top and bottom

    # Check glass (for windows) or panels (for doors)
    if 'glass' in phase_1b_spec:
        glass = phase_1b_spec['glass']
        glass_w = glass['width']
        glass_h = glass['height']

        tolerance = 0.001  # 1mm

        # Glass should EXACTLY match frame inner opening
        if abs(glass_w - frame_inner_w) > tolerance:
            result['passed'] = False
            result['errors'].append(
                f"Glass width ({glass_w}m) does NOT match frame inner width ({frame_inner_w}m). "
                f"Gap: {abs(glass_w - frame_inner_w)*1000:.1f}mm"
            )

        if abs(glass_h - frame_inner_h) > tolerance:
            result['passed'] = False
            result['errors'].append(
                f"Glass height ({glass_h}m) does NOT match frame inner height ({frame_inner_h}m). "
                f"Gap: {abs(glass_h - frame_inner_h)*1000:.1f}mm"
            )

    elif 'door_panels' in phase_1b_spec:
        # Double door
        panels = phase_1b_spec['door_panels']
        panel_w = panels['panel_width']
        panel_h = panels['panel_height']
        count = panels['count']
        gap = panels.get('center_gap', 0)

        # Total panel width (2 panels + center gap)
        total_panel_w = count * panel_w + gap

        tolerance = 0.001

        if abs(total_panel_w - frame_inner_w) > tolerance:
            result['passed'] = False
            result['errors'].append(
                f"Total panel width ({total_panel_w}m) does NOT match frame inner width ({frame_inner_w}m). "
                f"Gap: {abs(total_panel_w - frame_inner_w)*1000:.1f}mm"
            )

        if abs(panel_h - frame_inner_h) > tolerance:
            result['passed'] = False
            result['errors'].append(
                f"Panel height ({panel_h}m) does NOT match frame inner height ({frame_inner_h}m). "
                f"Gap: {abs(panel_h - frame_inner_h)*1000:.1f}mm"
            )

    elif 'door_panel' in phase_1b_spec:
        # Single door
        panel = phase_1b_spec['door_panel']
        panel_w = panel['width']
        panel_h = panel['height']

        tolerance = 0.001

        if abs(panel_w - frame_inner_w) > tolerance:
            result['passed'] = False
            result['errors'].append(
                f"Panel width ({panel_w}m) does NOT match frame inner width ({frame_inner_w}m). "
                f"Gap: {abs(panel_w - frame_inner_w)*1000:.1f}mm"
            )

        if abs(panel_h - frame_inner_h) > tolerance:
            result['passed'] = False
            result['errors'].append(
                f"Panel height ({panel_h}m) does NOT match frame inner height ({frame_inner_h}m). "
                f"Gap: {abs(panel_h - frame_inner_h)*1000:.1f}mm"
            )

    return result


def main():
    """Main verification function."""
    if 'iteration_num' not in globals():
        raise ValueError("iteration_num not set. Set it before running this script.")

    iteration = globals()['iteration_num']

    print("="*70)
    print(f" Phase 1B Verification - Iteration {iteration:03d}")
    print("="*70)
    print("\nVerifying that frames EXACTLY fill cutouts with NO GAPS\n")

    # Load specifications
    phase_1a_spec_path = scripts_dir.parent / 'work' / 'spec' / 'phase_1a' / 'building_geometry.yaml'
    with open(phase_1a_spec_path, 'r') as f:
        phase_1a_spec = yaml.safe_load(f)

    phase_1b_spec_path = scripts_dir.parent / 'work' / 'spec' / 'phase_1b' / 'opening_fill.yaml'
    with open(phase_1b_spec_path, 'r') as f:
        phase_1b_spec = yaml.safe_load(f)

    # Output directory for screenshots
    screenshot_dir = scripts_dir.parent / 'work' / 'verification' / f'phase_1b_iter_{iteration:03d}'

    # Define openings to verify
    openings = [
        {
            'name': 'front_left_display_window',
            'type': 'window',
            'normal': Vector((0, -1, 0))  # Facing forward (negative Y)
        },
        {
            'name': 'front_right_display_window',
            'type': 'window',
            'normal': Vector((0, -1, 0))
        },
        {
            'name': 'door_alcove_left_window',
            'type': 'window',
            'normal': None  # Angled wall, will calculate
        },
        {
            'name': 'door_alcove_right_window',
            'type': 'window',
            'normal': None  # Angled wall, will calculate
        },
        {
            'name': 'front_entry_door',
            'type': 'door',
            'normal': Vector((0, 1, 0))  # Facing back (positive Y, alcove back wall)
        },
        {
            'name': 'rear_service_door',
            'type': 'door',
            'normal': Vector((0, 1, 0))  # Facing back (positive Y)
        }
    ]

    verification_results = []
    all_passed = True

    for opening in openings:
        opening_name = opening['name']

        print(f"\n{'='*70}")
        print(f" Verifying: {opening_name}")
        print('='*70)

        # Get specs
        cutout_spec = phase_1a_spec['cutouts'][opening_name]
        opening_spec = phase_1b_spec[opening_name]

        # Verify dimensions
        print(f"\n[1] Checking frame dimensions...")
        result = verify_opening_fill(opening_name, cutout_spec, opening_spec)

        if result['passed']:
            print(f"  ✓ Frame dimensions EXACTLY match cutout (no gaps)")
        else:
            print(f"  ❌ GAPS DETECTED:")
            for error in result['errors']:
                print(f"     - {error}")
            all_passed = False

        if result['warnings']:
            print(f"  ⚠️  Warnings:")
            for warning in result['warnings']:
                print(f"     - {warning}")

        # Verify glass/panel fill
        print(f"\n[2] Checking glass/panel fill...")
        fill_result = verify_glass_panel_fill(opening_name, opening_spec)

        if fill_result['passed']:
            print(f"  ✓ Glass/panel EXACTLY fills frame inner opening (NO gaps)")
        else:
            print(f"  ❌ GAPS DETECTED:")
            for error in fill_result['errors']:
                print(f"     - {error}")
            all_passed = False

        verification_results.append(fill_result)

        # Position camera and capture screenshot
        print(f"\n[3] Capturing verification screenshot...")

        pos = cutout_spec['position']
        position = Vector((pos['x'], pos['y'], pos['z'] + cutout_spec['height']/2))
        size = (cutout_spec['width'], cutout_spec['height'])

        # Use specified normal or default
        normal = opening['normal'] if opening['normal'] else Vector((0, -1, 0))

        camera = setup_camera_for_opening(opening_name, position, size, normal)
        screenshot = capture_opening_screenshot(opening_name, screenshot_dir)

        print(f"  ✓ Screenshot saved: {screenshot.name}")

        verification_results.append(result)

    # Print summary
    print("\n" + "="*70)
    print(" VERIFICATION SUMMARY")
    print("="*70)

    passed_count = sum(1 for r in verification_results if r['passed'])
    failed_count = len(verification_results) - passed_count

    print(f"\n  Total openings: {len(verification_results)}")
    print(f"  Passed: {passed_count}")
    print(f"  Failed: {failed_count}")

    if all_passed:
        print("\n✅ VERDICT: ALL FRAMES EXACTLY FILL CUTOUTS (NO GAPS)")

        # Create checkpoint
        checkpoint_data = {
            'iteration': iteration,
            'verification_results': verification_results,
            'passed_count': passed_count,
            'failed_count': failed_count,
            'screenshots_dir': str(screenshot_dir)
        }

        create_checkpoint(
            f"phase_1b_verification_{iteration:03d}",
            checkpoint_data
        )

        return 0
    else:
        print("\n❌ VERDICT: GAPS DETECTED - FRAMES DO NOT FILL CUTOUTS")
        print("\nFailed openings:")
        for r in verification_results:
            if not r['passed']:
                print(f"\n  - {r['opening']}:")
                for error in r['errors']:
                    print(f"    {error}")

        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
