"""
Geometry Validation Script

Reads metrics JSON output from Blender build and validates geometry quality.
Can run standalone (outside Blender) for CI/CD validation.

Usage:
    python validate_geometry.py --metrics work/metrics/metrics_001.json
"""

import argparse
import json
import sys
from pathlib import Path


class GeometryValidator:
    """Validates geometry metrics against quality standards."""

    def __init__(self, metrics):
        """
        Initialize validator with metrics dictionary.

        Args:
            metrics: Dictionary from metrics JSON file
        """
        self.metrics = metrics
        self.errors = []
        self.warnings = []

    def check_non_manifold(self):
        """
        Check for non-manifold edges.

        TODO: Implement check
        TODO: Non-manifold edges should be 0 for watertight geometry
        """
        print("TODO: check_non_manifold()")

        non_manifold = self.metrics.get("non_manifold_edges", 0)
        if non_manifold > 0:
            self.errors.append(f"Found {non_manifold} non-manifold edges")

    def check_intersections(self):
        """
        Check for intersecting faces.

        TODO: Implement check
        TODO: Intersecting faces indicate geometry errors
        """
        print("TODO: check_intersections()")

        intersecting = self.metrics.get("intersecting_faces", 0)
        if intersecting > 0:
            self.errors.append(f"Found {intersecting} intersecting faces")

    def check_coplanar_faces(self):
        """
        Check for excessive coplanar faces.

        TODO: Implement check
        TODO: Too many coplanar faces might indicate mesh optimization issues
        """
        print("TODO: check_coplanar_faces()")

        # Coplanar faces aren't necessarily bad, but could indicate optimization opportunities
        pass

    def check_dimension_errors(self):
        """
        Check if actual dimensions match spec within tolerance.

        TODO: Implement check
        TODO: Read dimension_errors from metrics
        TODO: Flag any dimensions outside tolerance
        """
        print("TODO: check_dimension_errors()")

        dim_errors = self.metrics.get("dimension_errors", [])
        if dim_errors:
            for error in dim_errors:
                self.errors.append(f"Dimension error: {error}")

    def check_face_count(self):
        """
        Check if face count is reasonable.

        TODO: Implement check
        TODO: Too few faces = overly simplified
        TODO: Too many faces = performance issues
        """
        print("TODO: check_face_count()")

        face_count = self.metrics.get("face_count", 0)

        # Arbitrary limits for now
        if face_count < 10:
            self.warnings.append(f"Very low face count: {face_count}")
        elif face_count > 100000:
            self.warnings.append(f"High face count: {face_count} (may impact performance)")

    def validate(self):
        """
        Run all validation checks.

        Returns:
            bool: True if validation passed (no errors)
        """
        print("Running geometry validation checks...")

        self.check_non_manifold()
        self.check_intersections()
        self.check_coplanar_faces()
        self.check_dimension_errors()
        self.check_face_count()

        return len(self.errors) == 0

    def print_report(self):
        """Print validation report to stdout."""
        print("\n" + "=" * 60)
        print("GEOMETRY VALIDATION REPORT")
        print("=" * 60)

        print(f"\nMetrics Summary:")
        print(f"  Vertices: {self.metrics.get('vertex_count', 'N/A')}")
        print(f"  Faces: {self.metrics.get('face_count', 'N/A')}")
        print(f"  Edges: {self.metrics.get('edge_count', 'N/A')}")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print(f"\n✅ No errors found")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        else:
            print(f"\n✅ No warnings")

        # Include any warnings from metrics generation
        metric_warnings = self.metrics.get("warnings", [])
        if metric_warnings:
            print(f"\n⚠️  METRICS WARNINGS:")
            for warning in metric_warnings:
                print(f"  - {warning}")

        print("\n" + "=" * 60)

        if len(self.errors) == 0:
            print("VALIDATION PASSED ✅")
        else:
            print("VALIDATION FAILED ❌")

        print("=" * 60 + "\n")


def load_metrics(metrics_path):
    """
    Load metrics JSON file.

    Args:
        metrics_path: Path to metrics JSON file

    Returns:
        dict: Metrics dictionary
    """
    with open(metrics_path, 'r') as f:
        return json.load(f)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate geometry metrics")
    parser.add_argument("--metrics", required=True, help="Path to metrics JSON file")
    return parser.parse_args()


def main():
    """Main execution."""
    args = parse_args()

    metrics_path = Path(args.metrics)
    if not metrics_path.exists():
        print(f"ERROR: Metrics file not found: {metrics_path}")
        sys.exit(1)

    print(f"Loading metrics from: {metrics_path}")
    metrics = load_metrics(metrics_path)

    validator = GeometryValidator(metrics)
    passed = validator.validate()
    validator.print_report()

    # Exit with appropriate code
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
