"""Concurrent async client load test against GET /async.

Uses asyncio + httpx.AsyncClient (no one-thread-per-request).
For N concurrent requests that each wait ~5s, expect total time ≈ 5 seconds.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time

import httpx

DEFAULT_URL = "http://127.0.0.1:8000/async"
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


async def _one_request(
    client: httpx.AsyncClient,
    url: str,
    index: int,
    total: int,
) -> tuple[bool, float]:
    """Return (success, elapsed_seconds). Never raises."""
    start = time.perf_counter()
    try:
        response = await client.get(url)
        elapsed = time.perf_counter() - start
        if response.is_success:
            return True, elapsed
        print(
            f"  Request {index}/{total}: HTTP {response.status_code} ({elapsed:.2f}s)",
            file=sys.stderr,
        )
        return False, elapsed
    except httpx.TimeoutException as exc:
        elapsed = time.perf_counter() - start
        print(
            f"  Request {index}/{total}: timeout after {elapsed:.2f}s — {exc}",
            file=sys.stderr,
        )
        return False, elapsed
    except httpx.RequestError as exc:
        elapsed = time.perf_counter() - start
        print(
            f"  Request {index}/{total}: connection/request error "
            f"({elapsed:.2f}s) — {exc}",
            file=sys.stderr,
        )
        return False, elapsed


async def _run_async(
    num_requests: int,
    url: str,
    timeout: float,
) -> dict:
    successful = 0
    failed = 0
    durations: list[float] = []

    overall_start = time.perf_counter()

    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [
            _one_request(client, url, i, num_requests)
            for i in range(1, num_requests + 1)
        ]
        results = await asyncio.gather(*tasks)

    total_time = time.perf_counter() - overall_start

    for ok, elapsed in results:
        if ok:
            successful += 1
            durations.append(elapsed)
        else:
            failed += 1

    return {
        "requests": num_requests,
        "successful": successful,
        "failed": failed,
        "total_time": total_time,
        "durations": durations,
    }


def run_async_test(
    num_requests: int,
    url: str = DEFAULT_URL,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """Run concurrent GET requests and return summary metrics."""
    return asyncio.run(_run_async(num_requests, url, timeout))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Concurrent async load test against the /async endpoint.",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=10,
        choices=[1, 5, 10, 20, 50],
        help="Number of concurrent requests (default: 10).",
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
        f"Starting concurrent async test: {args.requests} request(s) -> {args.url}\n"
    )
    result = run_async_test(args.requests, url=args.url, timeout=args.timeout)
    print_results(
        "Async Load Test",
        result["requests"],
        result["successful"],
        result["failed"],
        result["total_time"],
        result["durations"],
    )
    return 0 if result["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
