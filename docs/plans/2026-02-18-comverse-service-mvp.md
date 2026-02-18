# Comverse Service MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a FastAPI service that receives a mock WhatsApp message, calls a Lyzr ADK agent, and returns the response — validating the full conversational loop with session isolation per merchant+customer.

**Architecture:** A FastAPI app with a single `POST /chat` endpoint. Merchants are stored in-memory (mock). The Lyzr `Studio` is initialized once at app startup; `agent.run(message, session_id=...)` is called per message where `session_id = "{merchant_id}:{sender}"`. The lyzr service is dependency-injected so it can be mocked in tests.

**Tech Stack:** Python 3.11+, FastAPI, lyzr-adk, pytest, pytest-asyncio, httpx (for AsyncClient testing)

---

## Project Layout

```
comverse/service/
├── main.py
├── config.py
├── routes/
│   ├── __init__.py
│   └── chat.py
├── services/
│   ├── __init__.py
│   └── lyzr.py
├── mocks/
│   ├── __init__.py
│   └── merchants.py
├── models/
│   ├── __init__.py
│   └── chat.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_merchants.py
│   ├── test_models.py
│   ├── test_lyzr_service.py
│   └── test_chat_route.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── Makefile
```

---

### Task 1: Project Scaffold

**Files:**
- Create: `comverse/service/requirements.txt`
- Create: `comverse/service/requirements-dev.txt`
- Create: `comverse/service/.env.example`
- Create: `comverse/service/Makefile`
- Create: `comverse/service/.env` (from .env.example — not committed)

**Step 1: Create `requirements.txt`**

```
fastapi
uvicorn[standard]
lyzr-adk
pydantic-settings
python-dotenv
```

**Step 2: Create `requirements-dev.txt`**

```
pytest
pytest-asyncio
httpx
```

**Step 3: Create `.env.example`**

```
LYZR_API_KEY=
COMVERSE_AGENT_ID=
```

**Step 4: Create `Makefile`**

```makefile
.PHONY: dev test lint fmt

dev:
	uvicorn main:app --reload --port 8000

test:
	pytest tests/ -v

lint:
	ruff check .

fmt:
	ruff format .
```

**Step 5: Set up virtualenv and install**

```bash
cd comverse/service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env  # then fill in real values
```

Expected: no errors, packages installed.

**Step 6: Create empty `__init__.py` files**

```bash
mkdir -p routes services mocks models tests
touch routes/__init__.py services/__init__.py mocks/__init__.py models/__init__.py tests/__init__.py
```

**Step 7: Commit**

```bash
git init   # (only if not already a git repo)
git add requirements.txt requirements-dev.txt .env.example Makefile
git commit -m "chore: scaffold comverse service project"
```

---

### Task 2: Config Module

**Files:**
- Create: `comverse/service/config.py`
- Create: `comverse/service/tests/test_config.py`

**Step 1: Write the failing test**

`tests/test_config.py`:
```python
import os
import pytest
from config import Settings


def test_settings_loads_from_env(monkeypatch):
    monkeypatch.setenv("LYZR_API_KEY", "test-key-123")
    monkeypatch.setenv("COMVERSE_AGENT_ID", "agent-abc")

    settings = Settings()

    assert settings.lyzr_api_key == "test-key-123"
    assert settings.comverse_agent_id == "agent-abc"


def test_settings_raises_if_missing(monkeypatch):
    monkeypatch.delenv("LYZR_API_KEY", raising=False)
    monkeypatch.delenv("COMVERSE_AGENT_ID", raising=False)

    with pytest.raises(Exception):
        Settings()
```

**Step 2: Run to verify it fails**

```bash
pytest tests/test_config.py -v
```

Expected: `ModuleNotFoundError: No module named 'config'`

**Step 3: Write minimal implementation**

`config.py`:
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    lyzr_api_key: str
    comverse_agent_id: str

    class Config:
        env_file = ".env"


settings = Settings()
```

**Step 4: Run to verify it passes**

```bash
pytest tests/test_config.py -v
```

Expected: 2 PASSED

**Step 5: Commit**

```bash
git add config.py tests/test_config.py
git commit -m "feat: add config module with pydantic settings"
```

---

### Task 3: Mock Merchants

**Files:**
- Create: `comverse/service/mocks/merchants.py`
- Create: `comverse/service/tests/test_merchants.py`

**Step 1: Write the failing test**

`tests/test_merchants.py`:
```python
import pytest
from mocks.merchants import get_merchant, MerchantNotFoundError, Merchant


def test_get_known_merchant():
    merchant = get_merchant("merchant_001")
    assert isinstance(merchant, Merchant)
    assert merchant.name == "Amit's Cake Shop"
    assert merchant.catalog_summary is not None


def test_get_another_known_merchant():
    merchant = get_merchant("merchant_002")
    assert merchant.name == "Priya's Thali House"


def test_unknown_merchant_raises():
    with pytest.raises(MerchantNotFoundError):
        get_merchant("unknown_merchant")
```

**Step 2: Run to verify it fails**

```bash
pytest tests/test_merchants.py -v
```

Expected: `ModuleNotFoundError: No module named 'mocks.merchants'`

**Step 3: Write minimal implementation**

`mocks/merchants.py`:
```python
from dataclasses import dataclass


class MerchantNotFoundError(Exception):
    pass


@dataclass
class Merchant:
    id: str
    name: str
    catalog_summary: str


MOCK_MERCHANTS: dict[str, Merchant] = {
    "merchant_001": Merchant(
        id="merchant_001",
        name="Amit's Cake Shop",
        catalog_summary=(
            "Cakes: Chocolate (₹500), Vanilla (₹400), Red Velvet (₹600). "
            "Min order ₹300. Delivery in Pune. Order by 6pm for same-day."
        ),
    ),
    "merchant_002": Merchant(
        id="merchant_002",
        name="Priya's Thali House",
        catalog_summary=(
            "Thali: Veg (₹120), Non-veg (₹150). "
            "Open 11am–3pm. Minimum 2 thalis per order."
        ),
    ),
}


def get_merchant(merchant_id: str) -> Merchant:
    if merchant_id not in MOCK_MERCHANTS:
        raise MerchantNotFoundError(f"Merchant '{merchant_id}' not found")
    return MOCK_MERCHANTS[merchant_id]
```

**Step 4: Run to verify it passes**

```bash
pytest tests/test_merchants.py -v
```

Expected: 3 PASSED

**Step 5: Commit**

```bash
git add mocks/merchants.py tests/test_merchants.py
git commit -m "feat: add in-memory mock merchants"
```

---

### Task 4: Pydantic Models

**Files:**
- Create: `comverse/service/models/chat.py`
- Create: `comverse/service/tests/test_models.py`

**Step 1: Write the failing test**

`tests/test_models.py`:
```python
import pytest
from pydantic import ValidationError
from models.chat import ChatRequest, ChatResponse


def test_chat_request_valid():
    req = ChatRequest(merchant_id="merchant_001", sender="+919876543210", message="Hi")
    assert req.merchant_id == "merchant_001"
    assert req.sender == "+919876543210"
    assert req.message == "Hi"


def test_chat_request_requires_all_fields():
    with pytest.raises(ValidationError):
        ChatRequest(merchant_id="merchant_001")  # missing sender + message


def test_chat_response_valid():
    resp = ChatResponse(session_id="merchant_001:+919876543210", reply="Hello!")
    assert resp.session_id == "merchant_001:+919876543210"
    assert resp.reply == "Hello!"
```

**Step 2: Run to verify it fails**

```bash
pytest tests/test_models.py -v
```

Expected: `ModuleNotFoundError: No module named 'models.chat'`

**Step 3: Write minimal implementation**

`models/chat.py`:
```python
from pydantic import BaseModel


class ChatRequest(BaseModel):
    merchant_id: str
    sender: str   # customer phone number
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
```

**Step 4: Run to verify it passes**

```bash
pytest tests/test_models.py -v
```

Expected: 3 PASSED

**Step 5: Commit**

```bash
git add models/chat.py tests/test_models.py
git commit -m "feat: add chat request/response pydantic models"
```

---

### Task 5: Lyzr Service Wrapper

**Files:**
- Create: `comverse/service/services/lyzr.py`
- Create: `comverse/service/tests/test_lyzr_service.py`

**Step 1: Write the failing test**

`tests/test_lyzr_service.py`:
```python
from unittest.mock import MagicMock, patch
from services.lyzr import run_agent, init_lyzr


def test_run_agent_calls_lyzr_with_correct_args():
    mock_response = MagicMock()
    mock_response.response = "Here are our cakes!"

    mock_agent = MagicMock()
    mock_agent.run.return_value = mock_response

    reply = run_agent(
        agent=mock_agent,
        message="Show me your cakes",
        session_id="merchant_001:+919876543210",
    )

    mock_agent.run.assert_called_once_with(
        "Show me your cakes",
        session_id="merchant_001:+919876543210",
    )
    assert reply == "Here are our cakes!"


def test_run_agent_returns_response_string():
    mock_response = MagicMock()
    mock_response.response = "We have thali for ₹120"

    mock_agent = MagicMock()
    mock_agent.run.return_value = mock_response

    result = run_agent(
        agent=mock_agent,
        message="What do you have?",
        session_id="merchant_002:+911234567890",
    )

    assert isinstance(result, str)
    assert result == "We have thali for ₹120"
```

**Step 2: Run to verify it fails**

```bash
pytest tests/test_lyzr_service.py -v
```

Expected: `ModuleNotFoundError: No module named 'services.lyzr'`

**Step 3: Write minimal implementation**

`services/lyzr.py`:
```python
from lyzr import Studio


def init_lyzr(api_key: str, agent_id: str):
    """Initialize Studio and return the agent. Call once at app startup."""
    import os
    os.environ["LYZR_API_KEY"] = api_key
    studio = Studio()
    agent = studio.create_agent(
        name="Comverse Ordering Agent",
        provider="anthropic/claude-sonnet-4-5",
        role="WhatsApp commerce assistant for Indian SMBs",
        goal="Help customers browse catalog, place orders, and answer questions in Hinglish",
        instructions=(
            "Respond in Hinglish (mix of Hindi and English). "
            "Be warm, concise, and helpful. "
            "Guide customers through ordering step by step."
        ),
    )
    return agent


def run_agent(agent, message: str, session_id: str) -> str:
    """Send a message to the agent and return the text response."""
    response = agent.run(message, session_id=session_id)
    return response.response
```

> **Note on `init_lyzr`:** If a pre-existing agent ID already exists in Lyzr Studio, replace `studio.create_agent(...)` with `studio.get_agent(agent_id)` if the ADK supports it. Otherwise the agent is created fresh each startup (idempotent if given a stable name).

**Step 4: Run to verify it passes**

```bash
pytest tests/test_lyzr_service.py -v
```

Expected: 2 PASSED (no real Lyzr call — agent is mocked)

**Step 5: Commit**

```bash
git add services/lyzr.py tests/test_lyzr_service.py
git commit -m "feat: add lyzr service wrapper with run_agent()"
```

---

### Task 6: Chat Route

**Files:**
- Create: `comverse/service/routes/chat.py`
- Create: `comverse/service/tests/test_chat_route.py`
- Create: `comverse/service/tests/conftest.py`

**Step 1: Write the failing test**

`tests/conftest.py`:
```python
import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.chat import router, get_agent


@pytest.fixture
def mock_agent():
    agent = MagicMock()
    mock_response = MagicMock()
    mock_response.response = "Sure! We have Chocolate (₹500) and Vanilla (₹400)."
    agent.run.return_value = mock_response
    return agent


@pytest.fixture
def client(mock_agent):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_agent] = lambda: mock_agent
    return TestClient(app)
```

`tests/test_chat_route.py`:
```python
def test_chat_returns_reply(client, mock_agent):
    response = client.post("/chat", json={
        "merchant_id": "merchant_001",
        "sender": "+919876543210",
        "message": "Show me your cakes",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "Sure! We have Chocolate (₹500) and Vanilla (₹400)."
    assert data["session_id"] == "merchant_001:+919876543210"


def test_chat_uses_correct_session_id(client, mock_agent):
    client.post("/chat", json={
        "merchant_id": "merchant_002",
        "sender": "+911234567890",
        "message": "What thalis do you have?",
    })

    mock_agent.run.assert_called_once_with(
        "What thalis do you have?",
        session_id="merchant_002:+911234567890",
    )


def test_chat_unknown_merchant_returns_404(client):
    response = client.post("/chat", json={
        "merchant_id": "ghost_merchant",
        "sender": "+919999999999",
        "message": "Hello",
    })

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_chat_missing_fields_returns_422(client):
    response = client.post("/chat", json={"merchant_id": "merchant_001"})
    assert response.status_code == 422
```

**Step 2: Run to verify it fails**

```bash
pytest tests/test_chat_route.py -v
```

Expected: `ModuleNotFoundError: No module named 'routes.chat'`

**Step 3: Write minimal implementation**

`routes/chat.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from models.chat import ChatRequest, ChatResponse
from mocks.merchants import get_merchant, MerchantNotFoundError
from services.lyzr import run_agent

router = APIRouter()

# Dependency — overridden in tests and injected from app state in production
def get_agent():
    raise NotImplementedError("Agent not initialized")


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, agent=Depends(get_agent)):
    try:
        merchant = get_merchant(request.merchant_id)
    except MerchantNotFoundError:
        raise HTTPException(status_code=404, detail=f"Merchant '{request.merchant_id}' not found")

    session_id = f"{merchant.id}:{request.sender}"
    reply = run_agent(agent=agent, message=request.message, session_id=session_id)
    return ChatResponse(session_id=session_id, reply=reply)
```

**Step 4: Run to verify it passes**

```bash
pytest tests/test_chat_route.py -v
```

Expected: 4 PASSED

**Step 5: Commit**

```bash
git add routes/chat.py tests/test_chat_route.py tests/conftest.py
git commit -m "feat: add POST /chat route with merchant lookup and session isolation"
```

---

### Task 7: FastAPI App with Lifespan

**Files:**
- Create: `comverse/service/main.py`

> No dedicated test file — the route tests already cover endpoint behavior. The app wiring is verified in the smoke test below.

**Step 1: Write minimal implementation**

`main.py`:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings
from routes.chat import router, get_agent
from services.lyzr import init_lyzr


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Lyzr agent once at startup
    agent = init_lyzr(
        api_key=settings.lyzr_api_key,
        agent_id=settings.comverse_agent_id,
    )
    app.state.agent = agent
    # Override the dependency so routes use the real agent
    app.dependency_overrides[get_agent] = lambda: app.state.agent
    yield
    # Cleanup (nothing needed for now)


app = FastAPI(title="Comverse Service", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
```

**Step 2: Run smoke test (requires real .env values)**

```bash
make dev
# In another terminal:
curl http://localhost:8000/health
```

Expected: `{"status":"ok"}`

**Step 3: Run all tests to confirm nothing is broken**

```bash
pytest tests/ -v
```

Expected: all tests PASS (main.py is not imported in unit tests — they use TestClient directly)

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add fastapi app with lyzr lifespan initialization"
```

---

### Task 8: End-to-End Manual Smoke Test

> This is a manual verification with the real Lyzr API. Requires `.env` populated.

**Step 1: Start the server**

```bash
make dev
```

Expected: `Uvicorn running on http://127.0.0.1:8000`

**Step 2: Send a first message from a customer**

```bash
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"merchant_id": "merchant_001", "sender": "+919876543210", "message": "Hi, show me your cakes"}' \
  | python -m json.tool
```

Expected: JSON with `reply` referencing Amit's Cake Shop catalog.

**Step 3: Verify session continuity (follow-up message)**

```bash
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"merchant_id": "merchant_001", "sender": "+919876543210", "message": "How much is the red velvet?"}' \
  | python -m json.tool
```

Expected: Agent recalls it's a cake shop conversation and answers about Red Velvet (₹600).

**Step 4: Verify merchant isolation (same customer, different merchant)**

```bash
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"merchant_id": "merchant_002", "sender": "+919876543210", "message": "What do you serve?"}' \
  | python -m json.tool
```

Expected: Agent responds about Priya's Thali House — not cakes. Different session.

**Step 5: Commit with passing test run**

```bash
pytest tests/ -v
git add .
git commit -m "chore: verified end-to-end lyzr loop with session isolation"
```

---

## Summary

| Task | What it proves |
|------|---------------|
| 1. Scaffold | Project installs cleanly |
| 2. Config | Env vars load correctly |
| 3. Mock merchants | Merchant lookup works, unknown raises 404 |
| 4. Models | Request/response validation |
| 5. Lyzr wrapper | `agent.run()` is called with correct args |
| 6. Chat route | Full endpoint logic, session_id formation, 404 handling |
| 7. App | Lifespan wires real agent into dependency |
| 8. Smoke test | Real Lyzr call, session continuity, merchant isolation |

---

## Next Steps (after this plan)

- Replace `POST /chat` mock trigger with `POST /webhook` + `GET /webhook` (WhatsApp Cloud API signature verification)
- Replace `MOCK_MERCHANTS` with Neon DB `cv_merchants` table (asyncpg)
- Add `services/whatsapp.py` to deliver agent reply back via WhatsApp Cloud API
