"""Processing services for sync and async request handling demos."""

import asyncio
import time


def process_sync() -> dict:
    """Simulate a blocking (synchronous) operation lasting ~5 seconds."""
    start = time.perf_counter()
    time.sleep(5)
    duration = round(time.perf_counter() - start, 2)
    return {
        "mode": "sync",
        "message": "Processing completed",
        "duration": duration,
    }


async def process_async() -> dict:
    """Simulate a non-blocking (asynchronous) operation lasting ~5 seconds."""
    start = time.perf_counter()
    await asyncio.sleep(5)
    duration = round(time.perf_counter() - start, 2)
    return {
        "mode": "async",
        "message": "Processing completed",
        "duration": duration,
    }
