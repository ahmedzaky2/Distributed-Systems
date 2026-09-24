"""FastAPI application entry point — Stage 1: Sync vs Async."""

from fastapi import FastAPI

from app.services import process_async, process_sync

app = FastAPI(
    title="Scalable API Lab",
    description="Stage 1: Sync vs Async — demonstrating blocking vs non-blocking request handling.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/sync")
def sync_endpoint() -> dict:
    """Blocking endpoint that holds the worker for ~5 seconds."""
    return process_sync()


@app.get("/async")
async def async_endpoint() -> dict:
    """Non-blocking endpoint that awaits ~5 seconds without blocking the event loop."""
    return await process_async()
