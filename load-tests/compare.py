"""Run sequential sync and concurrent async load tests side by side.

Compares wall-clock totals for the same request count. Async is not
universally "faster" — the gain here comes from overlapping I/O waits.
"""

from __future__ import annotations

import argparse
import sys

from async_test import run_async_test
from sync_test import run_sync_test


def print_comparison(num_requests: int, sync: dict, async_result: dict) -> None:
    sync_time = sync["total_time"]
    async_time = async_result["total_time"]

    print("========================================")
    print("Sync vs Async Comparison")
    print("========================================")
    print()
    print(f"Requests: {num_requests}")
    print()
    print("Sync (sequential)")
    print("----------------------------------------")
    print(f"Total Time:       {sync_time:.2f} sec")
    print(f"Successful:       {sync['successful']}")
    print(f"Failed:           {sync['failed']}")
    print()
    print("Async (concurrent)")
    print("----------------------------------------")
    print(f"Total Time:       {async_time:.2f} sec")
    print(f"Successful:       {async_result['successful']}")
    print(f"Failed:           {async_result['failed']}")
    print()

    if sync_time > 0 and async_time > 0:
        speedup = sync_time / async_time
        print("Speedup")
        print("----------------------------------------")
        print(f"Sync / Async:     {speedup:.2f}x")
        print()
        print(
            "Note: Async is not universally faster. The improvement here comes from "
            "allowing multiple I/O-waiting operations to progress concurrently "
            "(simulated with sleep). This does not prove that async speeds up "
            "CPU-bound work."
        )
    else:
        print("Speedup: could not be calculated (zero total time).")

    print("========================================")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare sequential /sync vs concurrent /async load tests.",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=10,
        choices=[1, 5, 10, 20, 50],
        help="Number of requests for each test (default: 10).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    n = args.requests

    print(f"Running sync test ({n} sequential requests)...\n")
    sync_result = run_sync_test(n)
    print(
        f"  Sync done in {sync_result['total_time']:.2f}s "
        f"({sync_result['successful']} ok / {sync_result['failed']} failed)\n"
    )

    print(f"Running async test ({n} concurrent requests)...\n")
    async_result = run_async_test(n)
    print(
        f"  Async done in {async_result['total_time']:.2f}s "
        f"({async_result['successful']} ok / {async_result['failed']} failed)\n"
    )

    print_comparison(n, sync_result, async_result)

    if sync_result["failed"] or async_result["failed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
