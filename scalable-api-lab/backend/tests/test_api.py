"""Basic API tests for Stage 1 endpoints.

Trade-off note
--------------
The real /sync and /async handlers sleep for ~5 seconds. Running those
full sleeps in every test suite would make CI/local runs unnecessarily
slow. Instead, we override the service functions with fast stubs so we
still verify status codes, response shape, and mode — without waiting
10+ seconds per test run.

Full timing behavior is meant to be observed manually (or later with a
load tool such as Locust), not asserted in unit tests.
"""

from fastapi.testclient import TestClient

from app.main import app
from app import services


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sync(monkeypatch):
    def fake_process_sync():
        return {
            "mode": "sync",
            "message": "Processing completed",
            "duration": 0.01,
        }

    monkeypatch.setattr(services, "process_sync", fake_process_sync)
    # Re-bind the endpoint's reference used by the route
    monkeypatch.setattr("app.main.process_sync", fake_process_sync)

    response = client.get("/sync")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "sync"
    assert "duration" in body


def test_async(monkeypatch):
    async def fake_process_async():
        return {
            "mode": "async",
            "message": "Processing completed",
            "duration": 0.01,
        }

    monkeypatch.setattr(services, "process_async", fake_process_async)
    monkeypatch.setattr("app.main.process_async", fake_process_async)

    response = client.get("/async")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "async"
    assert "duration" in body
