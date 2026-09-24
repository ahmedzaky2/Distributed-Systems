# Scalable API Lab

An educational project that teaches **scalability concepts** step by step.

You start with a simple FastAPI app and gradually add concurrency experiments, a UI, queues, and more in later stages.

This repository currently includes **Stage 1** and **Stage 2**.

---

## Stage 1: Sync vs Async

Stage 1 demonstrates the practical difference between:

- **Synchronous** request handling (`time.sleep`)
- **Asynchronous** request handling (`asyncio.sleep`)

Both endpoints simulate work that takes about **5 seconds**.

### Sync vs Async — important concept

A single `/sync` request and a single `/async` request should both take approximately **5 seconds**.

**Async is not used to make the individual operation faster.**

The important difference appears when **multiple requests run concurrently** — that is Stage 2.

---

## Stage 2: Concurrent Request Testing

Stage 1 showed that a single sync and async request both take approximately 5 seconds.

Stage 2 introduces **multiple requests** and measures wall-clock time for:

- **Sequential execution** (client waits for each `/sync` call to finish before starting the next)
- **Concurrent asynchronous execution** (client fires many `/async` calls at once with `asyncio`)

### What we are testing

#### Sequential execution

```text
R1 ───── 5s
          R2 ───── 5s
                    R3 ───── 5s

Total ≈ 15s
```

#### Concurrent asynchronous execution

```text
R1 ───────── 5s ─────
R2 ───────── 5s ─────
R3 ───────── 5s ─────

Total ≈ 5s
```

### Expected approximate results

These values are **expected approximations**, not guaranteed measurements:

| Requests | Sync Total | Async Total |
|----------|------------|-------------|
| 1        | ~5 sec     | ~5 sec      |
| 5        | ~25 sec    | ~5 sec      |
| 10       | ~50 sec    | ~5 sec      |
| 20       | ~100 sec   | ~5 sec      |

### Important caveat

This lab uses **simulated I/O waiting** (`sleep`). It demonstrates concurrency for wait-heavy work. It should **not** be interpreted as proof that async makes **CPU-bound** work faster.

Async is not universally "faster" — the improvement here comes from allowing multiple I/O-waiting operations to progress at the same time.

### How to run Stage 2

1. Start the API (from `backend`, venv activated):

```bat
uvicorn app.main:app --reload
```

2. In another terminal, activate the same venv and run from `load-tests`:

**CMD:**

```bat
cd load-tests
..\backend\.venv\Scripts\activate.bat
python sync_test.py --requests 5
python async_test.py --requests 5
python compare.py --requests 5
```

**PowerShell:**

```powershell
cd load-tests
..\backend\.venv\Scripts\Activate.ps1
python sync_test.py --requests 5
python async_test.py --requests 5
python compare.py --requests 5
```

See `load-tests/README.md` for more detail.

---

## Requirements

- Windows
- Python 3.11+
- No Docker, WSL, Redis, or external databases for these stages

---

## Project structure

```text
Distributed-Systems/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app + routes
│   │   └── services.py      # Sync / async processing logic
│   ├── tests/
│   │   └── test_api.py
│   ├── requirements.txt
│   └── README.md
│
└── load-tests/
    ├── sync_test.py         # Sequential client → /sync
    ├── async_test.py        # Concurrent client → /async
    ├── compare.py           # Side-by-side comparison
    └── README.md
```

---

## Setup (Windows)

### 1. Create a virtual environment

**CMD:**

```bat
cd backend
python -m venv .venv
```

**PowerShell:**

```powershell
cd backend
python -m venv .venv
```

### 2. Activate the virtual environment

**CMD:**

```bat
.venv\Scripts\activate.bat
```

**PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run once (as Administrator if needed):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install dependencies

**CMD / PowerShell:**

```bat
pip install -r requirements.txt
```

`httpx` is included and is used by both the unit tests and the Stage 2 load scripts.

---

## Run the application

From the `backend` folder (with the venv activated):

**CMD / PowerShell:**

```bat
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## Available endpoints

| Method | Path     | Description                                      |
|--------|----------|--------------------------------------------------|
| GET    | `/health`| Health check                                     |
| GET    | `/sync`  | Blocking work (`time.sleep(5)`) — ~5 seconds     |
| GET    | `/async` | Non-blocking work (`asyncio.sleep(5)`) — ~5 sec  |

### Example responses

**GET `/health`**

```json
{
  "status": "ok"
}
```

**GET `/sync`**

```json
{
  "mode": "sync",
  "message": "Processing completed",
  "duration": 5.0
}
```

**GET `/async`**

```json
{
  "mode": "async",
  "message": "Processing completed",
  "duration": 5.0
}
```

---

## Swagger UI

With the server running, open:

```text
http://127.0.0.1:8000/docs
```

You should see:

- `GET /health`
- `GET /sync`
- `GET /async`

You can try each endpoint directly from Swagger.

---

## Run unit tests

From the `backend` folder (with the venv activated):

**CMD / PowerShell:**

```bat
pytest
```

### Test strategy note

The real handlers sleep for ~5 seconds. The automated tests **stub** the service functions so the suite stays fast while still checking:

- HTTP status `200`
- Expected `mode`
- Presence of `duration`

Wall-clock concurrency is measured with the Stage 2 scripts in `load-tests/`, not with unit tests.

---

## What is NOT included yet

Do **not** expect these yet — they come in later stages:

- React frontend (Stage 3+)
- Locust
- Load balancer / Nginx
- Redis
- Message queues / Celery / RabbitMQ
- Background workers
- Docker / Kubernetes
- Prometheus / Grafana

---

## Next steps

Stage 2 stops here. Stage 3 will introduce a React UI.
