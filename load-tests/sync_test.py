"""Sequential (blocking) client load test against GET /sync.

Sends requests one after another — no threads, no multiprocessing.
For N requests that each take ~5s, expect total time ≈ N * 5 seconds.
"""

from __future__ import annotations

import argparse
import sys
import time

import httpx

DEFAULT_URL = "http://127.0.0.1:8000/sync"
DEFAULT_TIMEOUT = 10.0


def print_results(
    title: str,
    requests: int,
    successful: int,
    failed: int,
    total_time: float,
    durations: list[float],
) -> None:
    average = (sum(durations) / len(durations)) if durations else 0.0
    rps = (successful / total_time) if total_time > 0 and successful else 0.0

    print("========================================")
    print(title)
    print("========================================")
    print(f"Requests:           {requests}")
    print(f"Successful:         {successful}")
    print(f"Failed:             {failed:>2}")
    print(f"Total Time:         {total_time:.2f} sec")
    print(f"Average Request:    {average:.2f} sec")
    print(f"Requests/sec:       {rps:.2f}")
    print("========================================")


def run_sync_test(
    num_requests: int,
    url: str = DEFAULT_URL,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """Run sequential GET requests and return summary metrics."""
    successful = 0
    failed = 0
    durations: list[float] = []

    overall_start = time.perf_counter()

    with httpx.Client(timeout=timeout) as client:
        for i in range(1, num_requests + 1):
            req_start = time.perf_counter()
            try:
                response = client.get(url)
                elapsed = time.perf_counter() - req_start
                if response.is_success:
                    successful += 1
                    durations.append(elapsed)
                else:
                    failed += 1
                    print(
                        f"  Request {i}/{num_requests}: "
                        f"HTTP {response.status_code} ({elapsed:.2f}s)",
                        file=sys.stderr,
                    )
            except httpx.TimeoutException as exc:
                failed += 1
                elapsed = time.perf_counter() - req_start
                print(
                    f"  Request {i}/{num_requests}: timeout after {elapsed:.2f}s — {exc}",
                    file=sys.stderr,
                )
            except httpx.RequestError as exc:
                failed += 1
                elapsed = time.perf_counter() - req_start
                print(
                    f"  Request {i}/{num_requests}: connection/request error "
                    f"({elapsed:.2f}s) — {exc}",
                    file=sys.stderr,
                )

    total_time = time.perf_counter() - overall_start

    return {
        "requests": num_requests,
        "successful": successful,
        "failed": failed,
        "total_time": total_time,
        "durations": durations,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sequential load test against the /sync endpoint.",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=10,
        choices=[1, 5, 10, 20, 50],
        help="Number of sequential requests (default: 10).",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Target URL (default: {DEFAULT_URL}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Per-request timeout in seconds (default: {DEFAULT_TIMEOUT}).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(
        f"Starting sequential sync test: {args.requests} request(s) -> {args.url}\n"
    )
    result = run_sync_test(args.requests, url=args.url, timeout=args.timeout)
    print_results(
        "Sync Load Test (Sequential)",
        result["requests"],
        result["successful"],
        result["failed"],
        result["total_time"],
        result["durations"],
    )
    return 0 if result["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
