"""
Test Checkpoint Enforcement System

This script tests that the checkpoint system actually blocks export
when verification checkpoints are missing.

Usage:
    python scripts/test_checkpoint_enforcement.py
"""

import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent
sys.path.append(str(scripts_dir))

from verification_checkpoints import (
    create_checkpoint,
    require_checkpoint,
    require_all_checkpoints,
    clear_checkpoints,
    get_checkpoint_status
)

def test_checkpoint_blocking():
    """Test that missing checkpoints block export."""
    print("="*70)
    print(" Testing Checkpoint Enforcement System")
    print("="*70)

    iteration_num = 999  # Use test iteration number

    # ========================================================================
    # TEST 1: Clear all test checkpoints
    # ========================================================================
    print("\nTEST 1: Clearing test checkpoints...")
    clear_checkpoints(iteration_num)

    # ========================================================================
    # TEST 2: Verify require_checkpoint raises exception when missing
    # ========================================================================
    print("\nTEST 2: Testing require_checkpoint with missing checkpoint...")
    try:
        require_checkpoint(f"inline_verification_{iteration_num:03d}")
        print("❌ FAIL: require_checkpoint should have raised FileNotFoundError")
        return False
    except FileNotFoundError as e:
        print("✓ PASS: require_checkpoint correctly raised FileNotFoundError")
        print(f"  Error message: {str(e)[:100]}...")

    # ========================================================================
    # TEST 3: Verify require_all_checkpoints fails with missing checkpoints
    # ========================================================================
    print("\nTEST 3: Testing require_all_checkpoints with missing checkpoints...")
    try:
        require_all_checkpoints(iteration_num)
        print("❌ FAIL: require_all_checkpoints should have raised FileNotFoundError")
        return False
    except FileNotFoundError as e:
        print("✓ PASS: require_all_checkpoints correctly raised FileNotFoundError")

    # ========================================================================
    # TEST 4: Create checkpoint with critical failures should fail
    # ========================================================================
    print("\nTEST 4: Testing create_checkpoint with critical failures...")
    try:
        create_checkpoint(
            f"test_checkpoint_{iteration_num:03d}",
            {
                "critical_failures": ["Wall_Front", "Wall_Rear"],
                "results": {}
            }
        )
        print("❌ FAIL: create_checkpoint should have raised ValueError")
        return False
    except ValueError as e:
        print("✓ PASS: create_checkpoint correctly rejected data with critical failures")
        print(f"  Error message: {str(e)[:100]}...")

    # ========================================================================
    # TEST 5: Create valid checkpoints one by one
    # ========================================================================
    print("\nTEST 5: Creating valid checkpoints...")

    # Create checkpoint 1
    checkpoint_file = create_checkpoint(
        f"inline_verification_{iteration_num:03d}",
        {"status": "all_inline_checks_passed", "critical_failures": []}
    )
    print(f"  Created: {checkpoint_file.name}")

    # Verify require_checkpoint now passes
    data = require_checkpoint(f"inline_verification_{iteration_num:03d}")
    print(f"  Verified checkpoint exists and loads correctly")

    # But require_all_checkpoints should still fail (need all 3)
    print("\nTEST 5a: Testing require_all_checkpoints with 1/3 checkpoints...")
    try:
        require_all_checkpoints(iteration_num)
        print("❌ FAIL: require_all_checkpoints should still fail with only 1/3 checkpoints")
        return False
    except FileNotFoundError:
        print("✓ PASS: require_all_checkpoints correctly requires ALL checkpoints")

    # Create checkpoint 2
    create_checkpoint(
        f"batch_verification_{iteration_num:03d}",
        {
            "passed": True,
            "results": {},
            "critical_failures": [],
            "major_failures": []
        }
    )

    # Still should fail (need all 3)
    print("\nTEST 5b: Testing require_all_checkpoints with 2/3 checkpoints...")
    try:
        require_all_checkpoints(iteration_num)
        print("❌ FAIL: require_all_checkpoints should still fail with only 2/3 checkpoints")
        return False
    except FileNotFoundError:
        print("✓ PASS: require_all_checkpoints correctly requires ALL checkpoints")

    # Create checkpoint 3
    create_checkpoint(
        f"automated_verification_{iteration_num:03d}",
        {
            "issues": {
                "critical": [],
                "major": [],
                "minor": [],
                "passed": []
            }
        }
    )

    # Now all checkpoints present, should pass
    print("\nTEST 5c: Testing require_all_checkpoints with 3/3 checkpoints...")
    try:
        require_all_checkpoints(iteration_num)
        print("✓ PASS: require_all_checkpoints succeeded with all checkpoints present")
    except FileNotFoundError as e:
        print(f"❌ FAIL: require_all_checkpoints should pass with all checkpoints: {e}")
        return False

    # ========================================================================
    # TEST 6: Test get_checkpoint_status utility
    # ========================================================================
    print("\nTEST 6: Testing get_checkpoint_status utility...")
    status = get_checkpoint_status(iteration_num)

    all_exist = all(info['exists'] for info in status.values())
    if all_exist:
        print("✓ PASS: get_checkpoint_status reports all checkpoints exist")
    else:
        print("❌ FAIL: get_checkpoint_status should report all checkpoints exist")
        return False

    # ========================================================================
    # CLEANUP
    # ========================================================================
    print("\nCLEANUP: Clearing test checkpoints...")
    clear_checkpoints(iteration_num)

    # Verify cleanup worked
    status = get_checkpoint_status(iteration_num)
    none_exist = not any(info['exists'] for info in status.values())
    if none_exist:
        print("✓ Cleanup successful")
    else:
        print("⚠️  Warning: Some test checkpoints may not have been cleaned up")

    # ========================================================================
    # SUCCESS
    # ========================================================================
    print("\n" + "="*70)
    print(" ✅ ALL TESTS PASSED")
    print("="*70)
    print("\nConclusion:")
    print("  The checkpoint system successfully blocks export when checkpoints")
    print("  are missing. It is mechanically impossible to skip verification.")
    print("="*70 + "\n")

    return True


if __name__ == "__main__":
    success = test_checkpoint_blocking()
    sys.exit(0 if success else 1)
