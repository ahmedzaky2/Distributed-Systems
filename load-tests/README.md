# Load Tests — Stage 2

Client-side scripts that measure **sequential** vs **concurrent** request behavior against the Stage 1 FastAPI API.

These are educational scripts, not a full load-testing framework (Locust comes later).

---

## Prerequisites

1. Start the API from `backend` (venv activated):

```bat
cd ..\backend
uvicorn app.main:app --reload
```

2. Keep the server running, then open another terminal for the load tests.

3. Use the same Python environment that has `httpx` installed (the backend `.venv`):

**CMD:**

```bat
cd load-tests
..\backend\.venv\Scripts\activate.bat
```

**PowerShell:**

```powershell
cd load-tests
..\backend\.venv\Scripts\Activate.ps1
```

---

## Scripts

| Script          | Target  | Client behavior                          |
|-----------------|---------|------------------------------------------|
| `sync_test.py`  | `/sync` | Sequential (one request after another)   |
| `async_test.py` | `/async`| Concurrent (`asyncio` + `httpx.AsyncClient`) |
| `compare.py`    | both    | Runs sync then async for the same N      |

Supported `--requests` values: `1`, `5`, `10`, `20`, `50`.

---

## Examples

```bat
python sync_test.py --requests 10
python async_test.py --requests 10
python compare.py --requests 10
```

---

## What to expect

| Requests | Sync total (sequential) | Async total (concurrent) |
|----------|-------------------------|--------------------------|
| 1        | ~5 sec                  | ~5 sec                   |
| 5        | ~25 sec                 | ~5 sec                   |
| 10       | ~50 sec                 | ~5 sec                   |
| 20       | ~100 sec                | ~5 sec                   |

These are **approximate** expectations. Machine load and scheduling overhead will vary.

Async is not making each individual call faster (~5s each). The wall-clock win comes from overlapping I/O waits.

---

## Error handling

Each request uses a **10 second** timeout. Connection errors, timeouts, and non-2xx HTTP responses are counted as failures; the script continues and still prints a summary.
