# Scalable API Lab

An educational backend project that teaches **scalability concepts** step by step.

You will start with a simple FastAPI app and gradually add concurrency tools, load testing, queues, and more in later stages.

This repository currently includes **Stage 1 only**.

---

## Stage 1: Sync vs Async

Stage 1 demonstrates the practical difference between:

- **Synchronous** request handling (`time.sleep`)
- **Asynchronous** request handling (`asyncio.sleep`)

Both endpoints simulate work that takes about **5 seconds**.

### Sync vs Async — important concept

A single `/sync` request and a single `/async` request should both take approximately **5 seconds**.

**Async is not used to make the individual operation faster.**

The important difference appears when **multiple requests run concurrently**:

| Scenario        | Sync                         | Async                                      |
|-----------------|------------------------------|--------------------------------------------|
| Single request  | ≈ 5 sec                      | ≈ 5 sec                                    |
| Many concurrent | Workers block on each sleep  | Event loop can interleave waiting work    |

Later stages will send concurrent requests so you can see that difference clearly.

For now, Stage 1 only implements the two endpoints and a health check.

---

## Requirements

- Windows
- Python 3.11+
- No Docker, WSL, Redis, or external databases for this stage

---

## Project structure

```text
scalable-api-lab/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py          # FastAPI app + routes
    │   └── services.py      # Sync / async processing logic
    ├── tests/
    │   └── test_api.py
    ├── requirements.txt
    └── README.md
```

---

## Setup (Windows)

### 1. Create a virtual environment

**CMD:**

```bat
cd scalable-api-lab\backend
python -m venv .venv
```

**PowerShell:**

```powershell
cd scalable-api-lab\backend
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

## Run tests

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

Full 5-second timing is meant to be observed manually (or with a load tool in a later stage), not asserted in every unit test run.

---

## What is NOT included yet

Do **not** expect these in Stage 1 — they come later:

- React frontend
- Locust / load testing
- Load balancer / Nginx
- Redis
- Message queues / Celery / RabbitMQ
- Background workers
- Docker / Kubernetes
- Prometheus / Grafana

---

## Next steps

Stage 1 stops here. Later stages will add concurrent load demos and more infrastructure, one concept at a time.
