"""
Gated Export Function - Phase 1A

This module provides an export function that REQUIRES all verification
checkpoints to exist before allowing GLB export.

This is the enforcement mechanism that makes it mechanically impossible
to export without completing verification.

Usage:
    from export_with_verification import export_glb_phase_1a

    # This will FAIL if any verification checkpoint is missing
    glb_file = export_glb_phase_1a(iteration_num=5)
"""

import bpy
import os
import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

from verification_checkpoints import require_all_checkpoints, get_checkpoint_status


def export_glb_phase_1a(iteration_num):
    """
    Export GLB with mandatory verification gates.

    This function enforces that ALL verification steps have been completed
    before allowing export. It will raise an exception if any checkpoint
    is missing, making it impossible to skip verification.

    GATES:
    1. Verification checkpoints (inline, batch, automated)
    2. Required objects present in scene
    3. GLB export

    Args:
        iteration_num (int): Iteration number (e.g., 5)

    Returns:
        str: Path to exported GLB file

    Raises:
        FileNotFoundError: If any verification checkpoint is missing
        ValueError: If required objects are missing from scene

    Example:
        >>> export_glb_phase_1a(5)
        ======================================================================
         Phase 1A GLB Export - Iteration 5
        ======================================================================

        GATE 1: Checking verification checkpoints...
        ✓ Checkpoint validated: inline_verification_005
        ✓ Checkpoint validated: batch_verification_005
        ✓ Checkpoint validated: automated_verification_005
        ✓ All verification checkpoints validated for iteration 5

        GATE 2: Checking scene has required objects...
        ✓ All 8 required objects present

        GATE 3: Exporting GLB...
        ✓ GLB exported: exports/glb/building_phase_1a_iter_005.glb (49.6 KB)

        ======================================================================
         EXPORT COMPLETE - All verification gates passed
        ======================================================================

        'exports/glb/building_phase_1a_iter_005.glb'
    """
    print(f"\n{'='*70}")
    print(f" Phase 1A GLB Export - Iteration {iteration_num}")
    print(f"{'='*70}")

    # ========================================================================
    # GATE 1: Verify all checkpoints exist
    # ========================================================================
    print("\nGATE 1: Checking verification checkpoints...")

    try:
        require_all_checkpoints(iteration_num)
    except FileNotFoundError as e:
        print(f"\n❌ EXPORT BLOCKED")
        print(f"{'='*70}")
        print(str(e))
        print(f"{'='*70}\n")

        # Show checkpoint status for debugging
        print("Checkpoint status:")
        status = get_checkpoint_status(iteration_num)
        for checkpoint_name, info in status.items():
            if info['exists']:
                print(f"  ✓ {checkpoint_name} (completed {info['timestamp']})")
            else:
                print(f"  ✗ {checkpoint_name} (NOT COMPLETED)")

        print("\nVerification steps required:")
        print("  1. Inline verification (verify each element as built)")
        print("  2. Batch verification (verify_all_objects)")
        print("  3. Automated verification (exec verify_phase_1a.py)")
        print("\nExport cannot proceed until ALL verification steps complete.\n")

        # Re-raise the exception to block export
        raise

    # ========================================================================
    # GATE 2: Verify scene has expected objects
    # ========================================================================
    print("GATE 2: Checking scene has required objects...")

    required_objects = [
        'Foundation',
        'Wall_Front', 'Wall_Rear', 'Wall_Left', 'Wall_Right',
        'Roof',
        'Canopy_Roof',
        'Chimney'
    ]

    missing = [obj for obj in required_objects if obj not in bpy.data.objects]

    if missing:
        raise ValueError(
            f"\n{'='*70}\n"
            f"❌ Scene missing required objects: {missing}\n"
            f"{'='*70}\n"
            f"Cannot export - geometry is incomplete.\n"
        )

    print(f"✓ All {len(required_objects)} required objects present")

    # ========================================================================
    # GATE 3: Export GLB
    # ========================================================================
    print("\nGATE 3: Exporting GLB...")

    # Ensure export directory exists
    export_dir = Path("exports/glb")
    export_dir.mkdir(parents=True, exist_ok=True)

    output_file = export_dir / f"building_phase_1a_iter_{iteration_num:03d}.glb"

    # Select all visible mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    selected_count = 0
    for obj in bpy.data.objects:
        if not obj.hide_viewport and obj.type == 'MESH':
            obj.select_set(True)
            selected_count += 1

    if selected_count == 0:
        raise ValueError("No mesh objects selected for export")

    print(f"  Selected {selected_count} objects for export")

    # Export GLB
    bpy.ops.export_scene.gltf(
        filepath=str(output_file),
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT'
    )

    # Verify export succeeded
    if not output_file.exists():
        raise IOError(f"Export failed - file not created: {output_file}")

    file_size = output_file.stat().st_size / 1024
    print(f"✓ GLB exported: {output_file.name} ({file_size:.1f} KB)")

    # ========================================================================
    # SUCCESS
    # ========================================================================
    print(f"\n{'='*70}")
    print(" EXPORT COMPLETE - All verification gates passed")
    print(f"{'='*70}\n")

    return str(output_file)


def export_blocked_message():
    """
    Display a message explaining why export is blocked.

    This is a helper function to provide clear feedback when verification
    steps are incomplete.
    """
    print(f"\n{'='*70}")
    print(" EXPORT BLOCKED - Verification Required")
    print(f"{'='*70}\n")
    print("You cannot export until all verification steps complete.\n")
    print("Required verification workflow:")
    print("  1. Build geometry")
    print("  2. Run inline verification → creates checkpoint 1")
    print("  3. Run batch verification → creates checkpoint 2")
    print("  4. Run automated verification → creates checkpoint 3")
    print("  5. Export GLB (requires all 3 checkpoints)")
    print("\nThis enforcement prevents skipping verification steps.\n")
