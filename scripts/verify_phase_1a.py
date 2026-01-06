"""
Phase 1A Verification Script

Verifies that the built geometry matches the spec file within acceptable tolerances.
Runs inside Blender after building the model.

Usage:
    # Inside Blender Python console or via MCP:
    exec(open('scripts/verify_phase_1a.py').read())

    # Or with explicit iteration number:
    iteration_num = 5
    exec(open('scripts/verify_phase_1a.py').read())

Returns:
    Prints verification report and sets exit code:
    - 0: All verifications passed
    - 1: Critical issues found (>10% error)
    - 2: Major issues found (5-10% error)

    Creates verification checkpoint on success.
"""

import bpy
import yaml
import sys
from pathlib import Path

# Add scripts to path for checkpoint system
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

from verification_checkpoints import create_checkpoint


def load_spec():
    """Load Phase 1A spec file."""
    spec_path = Path(__file__).parent.parent / 'work' / 'spec' / 'phase_1a' / 'building_geometry.yaml'

    with open(spec_path, 'r') as f:
        spec = yaml.safe_load(f)

    return spec


def verify_geometry(spec):
    """
    Verify built geometry against spec validation_targets.

    Returns:
        dict with verification results
    """
    targets = spec['validation_targets']
    scene = bpy.context.scene

    issues = {
        'critical': [],  # >10% error
        'major': [],     # 5-10% error
        'minor': [],     # <5% error
        'passed': []     # Within tolerance
    }

    # Map validation targets to object measurements
    # NOTE: Only including measurements that are currently implemented
    # Cutout dimensions (door/window sizes) are NOT included because
    # measuring Boolean-modified geometry requires more sophisticated analysis
    measurements = {
        # Overall dimensions - measured from bounding box
        'overall_width': measure_building_width(),
        'overall_depth': measure_building_depth(),
        'wall_height': measure_wall_height(),

        # Parapet heights
        'parapet_height_front': measure_parapet_front(),
        'parapet_height_middle': measure_parapet_middle(),

        # Canopy
        'canopy_width': measure_canopy_width(),
        'canopy_depth': measure_canopy_depth(),
        'canopy_post_count': count_canopy_posts(),

        # Chimney
        'chimney_total_height': measure_chimney_total_height(),
    }

    # Compare each measurement against target
    for key, expected in targets.items():
        if key not in measurements:
            continue  # Skip targets we can't measure yet

        actual = measurements[key]

        # For count-based targets (like canopy_post_count), exact match required
        if 'count' in key:
            if actual == expected:
                issues['passed'].append({
                    'dimension': key,
                    'expected': expected,
                    'actual': actual,
                    'error_pct': 0.0
                })
            else:
                issues['critical'].append({
                    'dimension': key,
                    'expected': expected,
                    'actual': actual,
                    'error_pct': 100.0,
                    'error_type': 'count_mismatch'
                })
            continue

        # For dimensional targets, calculate percentage error
        if expected == 0:
            continue  # Skip zero targets (like parapet_height_rear)

        error_pct = abs(actual - expected) / expected * 100

        issue = {
            'dimension': key,
            'expected': expected,
            'actual': actual,
            'error_pct': error_pct,
            'error_abs': abs(actual - expected)
        }

        if error_pct > 10:
            issues['critical'].append(issue)
        elif error_pct > 5:
            issues['major'].append(issue)
        elif error_pct > 1:
            issues['minor'].append(issue)
        else:
            issues['passed'].append(issue)

    return issues


def measure_building_width():
    """Measure overall building width from wall objects."""
    walls = [obj for obj in bpy.data.objects if 'Wall' in obj.name and obj.type == 'MESH']
    if not walls:
        return 0

    # Get X bounds
    x_coords = []
    for wall in walls:
        for v in wall.data.vertices:
            world_co = wall.matrix_world @ v.co
            x_coords.append(world_co.x)

    return max(x_coords) - min(x_coords) if x_coords else 0


def measure_building_depth():
    """Measure overall building depth from wall objects."""
    walls = [obj for obj in bpy.data.objects if 'Wall' in obj.name and obj.type == 'MESH']
    if not walls:
        return 0

    # Get Y bounds
    y_coords = []
    for wall in walls:
        for v in wall.data.vertices:
            world_co = wall.matrix_world @ v.co
            y_coords.append(world_co.y)

    return max(y_coords) - min(y_coords) if y_coords else 0


def measure_wall_height():
    """Measure wall height from wall objects."""
    walls = [obj for obj in bpy.data.objects if 'Wall' in obj.name and obj.type == 'MESH']
    if not walls:
        return 0

    # Get Z bounds - in spec coordinates Z=0 is base of walls (top of foundation)
    z_coords = []
    for wall in walls:
        for v in wall.data.vertices:
            world_co = wall.matrix_world @ v.co
            if world_co.z > 0.1:  # Above Z=0 (wall base)
                z_coords.append(world_co.z)

    return max(z_coords) if z_coords else 0  # Max Z is wall height (since walls start at Z=0)


def measure_parapet_front():
    """Measure front parapet height above roof."""
    parapet_objs = [obj for obj in bpy.data.objects if 'Parapet_Front' in obj.name or 'Parapet_Left_Front' in obj.name or 'Parapet_Right_Front' in obj.name]
    if not parapet_objs:
        return 0

    # Get max Z height
    max_z = max(
        max((obj.matrix_world @ v.co for v in obj.data.vertices), key=lambda co: co.z).z
        for obj in parapet_objs
    )

    roof_top = 3.75 + 0.20  # 3.95m
    return max_z - roof_top


def measure_parapet_middle():
    """Measure middle parapet height above roof."""
    parapet_objs = [obj for obj in bpy.data.objects if 'Parapet_Left_Middle' in obj.name or 'Parapet_Right_Middle' in obj.name]
    if not parapet_objs:
        return 0

    # Get max Z height
    max_z = max(
        max((obj.matrix_world @ v.co for v in obj.data.vertices), key=lambda co: co.z).z
        for obj in parapet_objs
    )

    roof_top = 3.75 + 0.20  # 3.95m
    return max_z - roof_top


def measure_canopy_width():
    """Measure canopy width."""
    canopy = bpy.data.objects.get('Canopy_Roof')
    if canopy:
        return canopy.dimensions.x
    return 0


def measure_canopy_depth():
    """Measure canopy depth."""
    canopy = bpy.data.objects.get('Canopy_Roof')
    if canopy:
        return canopy.dimensions.y
    return 0


def count_canopy_posts():
    """Count canopy support posts."""
    posts = [obj for obj in bpy.data.objects if 'Canopy_Post' in obj.name]
    return len(posts)


def measure_chimney_total_height():
    """Measure chimney total height from ground."""
    chimney = bpy.data.objects.get('Chimney')
    if not chimney:
        return 0

    # Get max Z coordinate
    max_z = max((chimney.matrix_world @ v.co for v in chimney.data.vertices), key=lambda co: co.z).z
    return max_z


def print_report(issues):
    """Print formatted verification report."""
    print("\n" + "="*70)
    print(" Phase 1A Dimensional Verification Report")
    print("="*70)

    # Critical issues
    if issues['critical']:
        print(f"\n❌ CRITICAL ISSUES ({len(issues['critical'])}):")
        print("   (>10% error - MUST FIX before proceeding)")
        for issue in issues['critical']:
            print(f"\n   - {issue['dimension']}:")
            print(f"     Expected: {issue['expected']}")
            print(f"     Actual:   {issue['actual']:.3f}")
            print(f"     Error:    {issue['error_pct']:.1f}%")

    # Major issues
    if issues['major']:
        print(f"\n⚠️  MAJOR ISSUES ({len(issues['major'])}):")
        print("   (5-10% error - should fix)")
        for issue in issues['major']:
            print(f"\n   - {issue['dimension']}:")
            print(f"     Expected: {issue['expected']}")
            print(f"     Actual:   {issue['actual']:.3f}")
            print(f"     Error:    {issue['error_pct']:.1f}%")

    # Minor issues
    if issues['minor']:
        print(f"\n⚡ MINOR ISSUES ({len(issues['minor'])}):")
        print("   (1-5% error - acceptable but could improve)")
        for issue in issues['minor']:
            print(f"   - {issue['dimension']}: {issue['error_pct']:.1f}% error")

    # Passed
    if issues['passed']:
        print(f"\n✓ PASSED ({len(issues['passed'])} dimensions within tolerance)")

    # Summary
    print("\n" + "-"*70)
    print(" SUMMARY:")
    print(f"   Critical: {len(issues['critical'])}")
    print(f"   Major:    {len(issues['major'])}")
    print(f"   Minor:    {len(issues['minor'])}")
    print(f"   Passed:   {len(issues['passed'])}")
    print("="*70)

    # Verdict
    if issues['critical']:
        print("\n❌ VERDICT: FAILED - Critical issues must be fixed")
        return 1
    elif issues['major']:
        print("\n⚠️  VERDICT: PASSED WITH WARNINGS - Major issues should be addressed")
        return 2
    else:
        print("\n✅ VERDICT: PASSED - Geometry meets specification")
        return 0


def main():
    """Main verification function."""
    print("Loading Phase 1A specification...")
    spec = load_spec()

    print("Verifying geometry...")
    issues = verify_geometry(spec)

    exit_code = print_report(issues)

    # Create verification checkpoint if passed
    if exit_code == 0:
        # Try to get iteration number from global scope
        # (should be set before running this script: iteration_num = 5)
        import __main__
        iteration_num = getattr(__main__, 'iteration_num', None)

        if iteration_num is None:
            # Fall back to reading from phase_state.json
            try:
                import json
                phase_state_path = Path(__file__).parent.parent / 'work' / 'phase_state.json'
                with open(phase_state_path) as f:
                    phase_state = json.load(f)
                iteration_num = phase_state.get('current_iteration', 0)
            except Exception as e:
                print(f"\n⚠️  WARNING: Could not determine iteration number: {e}")
                print("Checkpoint not created. Set 'iteration_num' variable before running script.")
                return exit_code

        # Create checkpoint
        try:
            create_checkpoint(
                f"automated_verification_{iteration_num:03d}",
                {
                    "issues": issues,
                    "critical_count": len(issues['critical']),
                    "major_count": len(issues['major']),
                    "minor_count": len(issues['minor']),
                    "passed_count": len(issues['passed'])
                }
            )
        except Exception as e:
            print(f"\n⚠️  WARNING: Failed to create checkpoint: {e}")

    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
