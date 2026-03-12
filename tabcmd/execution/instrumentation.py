"""
Instrumentation module for tracking REST API call performance.
"""
import time
import re
from typing import Dict, List, Tuple
from collections import defaultdict


class APIInstrumenter:
    """
    Tracks timing statistics for REST API calls.
    """

    def __init__(self):
        self.enabled = False
        self.calls: List[Tuple[str, str, float, bool]] = []  # [(method, path, duration, success)]

    def enable(self):
        """Enable instrumentation tracking."""
        self.enabled = True

    def record_call(self, method: str, url: str, duration: float, success: bool = True):
        """
        Record an API call with its timing information.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full URL of the request
            duration: Time taken in seconds
            success: Whether the call succeeded
        """
        if not self.enabled:
            return

        # Normalize the path by replacing IDs with placeholders
        path = self._normalize_path(url)
        self.calls.append((method, path, duration, success))

    def _normalize_path(self, url: str) -> str:
        """
        Normalize URL path by replacing dynamic segments with placeholders.

        Example:
            /api/3.0/sites/abc123/workbooks/def456
            -> /api/3.0/sites/{site-id}/workbooks/{workbook-id}
        """
        # Extract just the path from the URL
        if "://" in url:
            # Remove scheme and host
            path = "/" + url.split("://", 1)[1].split("/", 1)[1] if "/" in url.split("://", 1)[1] else ""
        else:
            path = url

        # Remove query parameters
        path = path.split("?")[0]

        # Replace common ID patterns with placeholders
        # UUIDs and long alphanumeric strings
        path = re.sub(
            r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "/{id}", path, flags=re.IGNORECASE
        )

        # Contextual replacements based on preceding path segment
        path = re.sub(r"/sites/[^/]+(?=/|$)", "/sites/{site-id}", path)
        path = re.sub(r"/workbooks/[^/]+(?=/|$)", "/workbooks/{workbook-id}", path)
        path = re.sub(r"/datasources/[^/]+(?=/|$)", "/datasources/{datasource-id}", path)
        path = re.sub(r"/views/[^/]+(?=/|$)", "/views/{view-id}", path)
        path = re.sub(r"/projects/[^/]+(?=/|$)", "/projects/{project-id}", path)
        path = re.sub(r"/users/[^/]+(?=/|$)", "/users/{user-id}", path)
        path = re.sub(r"/groups/[^/]+(?=/|$)", "/groups/{group-id}", path)
        path = re.sub(r"/schedules/[^/]+(?=/|$)", "/schedules/{schedule-id}", path)
        path = re.sub(r"/jobs/[^/]+(?=/|$)", "/jobs/{job-id}", path)
        path = re.sub(r"/tasks/[^/]+(?=/|$)", "/tasks/{task-id}", path)

        # Catch any remaining alphanumeric IDs that weren't caught above
        # This looks for path segments that are purely alphanumeric (likely IDs)
        path = re.sub(r"/[a-zA-Z0-9_-]{10,}(?=/|$)", "/{id}", path)

        return path

    def print_statistics(self):
        """
        Print formatted statistics about API calls.
        """
        if not self.enabled or not self.calls:
            return

        # Group calls by endpoint (method + path) and success status
        endpoint_stats: Dict[Tuple[str, str], Dict[str, any]] = defaultdict(
            lambda: {"times": [], "success_count": 0, "failure_count": 0}
        )

        for method, path, duration, success in self.calls:
            key = (method, path)
            endpoint_stats[key]["times"].append(duration)
            if success:
                endpoint_stats[key]["success_count"] += 1
            else:
                endpoint_stats[key]["failure_count"] += 1

        # Calculate statistics and sort by total time
        results = []
        for (method, path), stats in endpoint_stats.items():
            times = stats["times"]
            total_time = sum(times)
            count = len(times)
            min_time = min(times)
            max_time = max(times)
            mean_time = total_time / count if count > 0 else 0

            results.append(
                {
                    "endpoint": f"{method} {path}",
                    "count": count,
                    "success": stats["success_count"],
                    "failure": stats["failure_count"],
                    "min": min_time,
                    "mean": mean_time,
                    "max": max_time,
                    "total": total_time,
                }
            )

        # Sort by total time descending
        results.sort(key=lambda x: x["total"], reverse=True)

        # Print formatted output
        print("\n" + "=" * 120)
        print("REST API Call Statistics:")
        print("=" * 120)

        # Header
        header = f"{'Endpoint':<60} {'Count':>7} {'Success':>7} {'Failure':>7} {'Min(s)':>9} {'Mean(s)':>9} {'Max(s)':>9} {'Total(s)':>10}"
        print(header)
        print("-" * 120)

        # Data rows
        for result in results:
            row = (
                f"{result['endpoint']:<60} "
                f"{result['count']:>7} "
                f"{result['success']:>7} "
                f"{result['failure']:>7} "
                f"{result['min']:>9.3f} "
                f"{result['mean']:>9.3f} "
                f"{result['max']:>9.3f} "
                f"{result['total']:>10.3f}"
            )
            print(row)

        # Summary
        print("-" * 120)
        total_calls = len(self.calls)
        total_time = sum(duration for _, _, duration, _ in self.calls)
        total_success = sum(1 for _, _, _, success in self.calls if success)
        total_failure = total_calls - total_success

        print(
            f"{'TOTAL':<60} {total_calls:>7} {total_success:>7} {total_failure:>7} "
            f"{'-':>9} {'-':>9} {'-':>9} {total_time:>10.3f}"
        )
        print("=" * 120 + "\n")


# Global instance
_instrumenter = APIInstrumenter()


def get_instrumenter() -> APIInstrumenter:
    """Get the global instrumenter instance."""
    return _instrumenter
