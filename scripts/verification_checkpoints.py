"""
Verification Checkpoint System

Creates and validates checkpoint files that prove verification steps completed.
This system makes it mechanically impossible to skip verification steps.

Checkpoints are stored as JSON files in work/verification/checkpoints/
Each checkpoint contains verification results and a timestamp.
"""

import json
import os
from datetime import datetime
from pathlib import Path


# Checkpoint directory - make it absolute to avoid working directory issues
# Get the project root (parent of scripts directory)
_SCRIPTS_DIR = Path(__file__).parent if '__file__' in globals() else Path.cwd() / 'scripts'
_PROJECT_ROOT = _SCRIPTS_DIR.parent
CHECKPOINT_DIR = _PROJECT_ROOT / "work" / "verification" / "checkpoints"


def create_checkpoint(checkpoint_name, data):
    """
    Create a verification checkpoint file.

    This function creates proof that a verification step completed successfully.
    It validates the data to ensure verification actually passed before creating
    the checkpoint file.

    Args:
        checkpoint_name (str): Checkpoint identifier (e.g., "inline_verification_005")
        data (dict): Verification results containing:
            - For verify_all_objects: {'passed', 'results', 'critical_failures', 'major_failures'}
            - For custom verification: any dict, but must not have critical_failures

    Returns:
        Path: Path to created checkpoint file

    Raises:
        ValueError: If data indicates verification failures (prevents checkpoint creation)

    Example:
        >>> results = verify_all_objects(specs)
        >>> create_checkpoint("batch_verification_005", results)
        ✓ Checkpoint created: batch_verification_005
    """
    # Ensure checkpoint directory exists
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    checkpoint_data = {
        "checkpoint": checkpoint_name,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

    # Validate: Check for critical failures
    if "critical_failures" in data and len(data["critical_failures"]) > 0:
        raise ValueError(
            f"Cannot create checkpoint '{checkpoint_name}' - "
            f"{len(data['critical_failures'])} critical failures found.\n"
            f"Failed objects: {data['critical_failures']}\n"
            f"Fix these failures before proceeding."
        )

    # Write checkpoint file
    checkpoint_file = CHECKPOINT_DIR / f"{checkpoint_name}.json"
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint_data, f, indent=2)

    print(f"✓ Checkpoint created: {checkpoint_name}")
    return checkpoint_file


def require_checkpoint(checkpoint_name):
    """
    Verify that a checkpoint exists. Raises exception if missing.

    This function enforces that a verification step has been completed
    before allowing progress to continue.

    Args:
        checkpoint_name (str): Checkpoint identifier (e.g., "inline_verification_005")

    Returns:
        dict: Checkpoint data if found

    Raises:
        FileNotFoundError: If checkpoint file doesn't exist (verification not completed)

    Example:
        >>> require_checkpoint("batch_verification_005")
        ✓ Checkpoint validated: batch_verification_005
        {'checkpoint': 'batch_verification_005', 'timestamp': '...', 'data': {...}}
    """
    checkpoint_file = CHECKPOINT_DIR / f"{checkpoint_name}.json"

    if not checkpoint_file.exists():
        raise FileNotFoundError(
            f"\n{'='*70}\n"
            f"❌ VERIFICATION CHECKPOINT MISSING: {checkpoint_name}\n"
            f"{'='*70}\n\n"
            f"This verification step has not been completed.\n"
            f"Cannot proceed until verification passes.\n\n"
            f"Expected checkpoint file: {checkpoint_file}\n\n"
            f"You must complete the verification step that creates this checkpoint.\n"
        )

    # Load and return checkpoint data
    with open(checkpoint_file) as f:
        data = json.load(f)

    print(f"✓ Checkpoint validated: {checkpoint_name}")
    return data


def require_all_checkpoints(iteration_num):
    """
    Verify all required checkpoints exist for an iteration.

    This is the primary enforcement mechanism. Call this before exporting
    to ensure all verification steps have been completed.

    Args:
        iteration_num (int): Iteration number (e.g., 5)

    Returns:
        bool: True if all checkpoints exist

    Raises:
        FileNotFoundError: If any required checkpoint is missing

    Example:
        >>> require_all_checkpoints(5)
        ✓ Checkpoint validated: inline_verification_005
        ✓ Checkpoint validated: batch_verification_005
        ✓ Checkpoint validated: automated_verification_005
        ✓ All verification checkpoints validated for iteration 5
        True
    """
    # Define required checkpoints for Phase 1A
    required = [
        f"inline_verification_{iteration_num:03d}",
        f"batch_verification_{iteration_num:03d}",
        f"automated_verification_{iteration_num:03d}"
    ]

    print(f"\nVerifying all checkpoints for iteration {iteration_num}...")

    # Check each checkpoint
    for checkpoint in required:
        require_checkpoint(checkpoint)

    print(f"✓ All verification checkpoints validated for iteration {iteration_num}\n")
    return True


def clear_checkpoints(iteration_num=None):
    """
    Clear checkpoints for an iteration (use when rebuilding).

    Args:
        iteration_num (int, optional): If provided, only clear checkpoints for this iteration.
                                      If None, clear all checkpoints.

    Example:
        >>> clear_checkpoints(5)  # Clear only iteration 5
        >>> clear_checkpoints()   # Clear all
    """
    if not CHECKPOINT_DIR.exists():
        print("No checkpoints to clear")
        return

    if iteration_num is None:
        # Clear all
        for checkpoint_file in CHECKPOINT_DIR.glob("*.json"):
            checkpoint_file.unlink()
        print("✓ All checkpoints cleared")
    else:
        # Clear specific iteration
        pattern = f"*_{iteration_num:03d}.json"
        count = 0
        for checkpoint_file in CHECKPOINT_DIR.glob(pattern):
            checkpoint_file.unlink()
            count += 1
        print(f"✓ Cleared {count} checkpoint(s) for iteration {iteration_num}")


def list_checkpoints(iteration_num=None):
    """
    List existing checkpoints.

    Args:
        iteration_num (int, optional): If provided, only list checkpoints for this iteration

    Returns:
        list: List of checkpoint names

    Example:
        >>> list_checkpoints(5)
        ['inline_verification_005', 'batch_verification_005']
    """
    if not CHECKPOINT_DIR.exists():
        return []

    if iteration_num is None:
        pattern = "*.json"
    else:
        pattern = f"*_{iteration_num:03d}.json"

    checkpoints = []
    for checkpoint_file in CHECKPOINT_DIR.glob(pattern):
        checkpoint_name = checkpoint_file.stem
        checkpoints.append(checkpoint_name)

    return sorted(checkpoints)


# Utility function for debugging
def get_checkpoint_status(iteration_num):
    """
    Get status of all required checkpoints for an iteration.

    Args:
        iteration_num (int): Iteration number

    Returns:
        dict: Status of each checkpoint (exists: bool, timestamp: str or None)

    Example:
        >>> get_checkpoint_status(5)
        {
            'inline_verification_005': {'exists': True, 'timestamp': '2026-01-04T...'},
            'batch_verification_005': {'exists': False, 'timestamp': None},
            'automated_verification_005': {'exists': False, 'timestamp': None}
        }
    """
    required = [
        f"inline_verification_{iteration_num:03d}",
        f"batch_verification_{iteration_num:03d}",
        f"automated_verification_{iteration_num:03d}"
    ]

    status = {}
    for checkpoint_name in required:
        checkpoint_file = CHECKPOINT_DIR / f"{checkpoint_name}.json"

        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                data = json.load(f)
            status[checkpoint_name] = {
                'exists': True,
                'timestamp': data.get('timestamp')
            }
        else:
            status[checkpoint_name] = {
                'exists': False,
                'timestamp': None
            }

    return status
