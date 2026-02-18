# Comverse

**Commerce + Converse** — WhatsApp conversational commerce for Indian SMBs.

Enables catalog-based food businesses (cake shops, cafes, thali restaurants) to take orders directly on WhatsApp at **10% commission** vs 25–35% on Zomato/Swiggy. A Hinglish AI agent handles the full ordering journey — no new app needed for customers.

---

## How It Works

```
Customer (WhatsApp)
        │
        ▼
WhatsApp Cloud API ──► Comverse Service (FastAPI) ──► Lyzr Agent (Claude Sonnet)
                                │
                                ▼
                        Supabase (orders, catalog)
```

---

## Repo Structure

```
comverse/
├── service/        # FastAPI backend (webhook handler + Lyzr caller)
├── demo/           # Streamlit demo UI (simulates WhatsApp chat)
└── docs/           # OpenAPI specs, plans
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- A [Lyzr Studio](https://studio.lyzr.ai) account and API key

---

### 1. Backend service

```bash
cd service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The backend starts fine with **no `.env`** — you can provide your Lyzr key via the demo UI instead. Optionally pre-configure via environment:

```bash
cp .env.example .env
# Edit .env and set LYZR_API_KEY=your-key-here
```

Start the server:

```bash
make dev
# or: uvicorn main:app --reload --port 8000
```

API runs at `http://localhost:8000`. Health check: `GET /health`

---

### 2. Demo UI

```bash
cd demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

**First time:** click **⚙️ Settings** in the sidebar, paste your Lyzr API key, and hit Save. The backend will create a Lyzr agent on the first message and reuse it for the session.

---

## API

### `POST /chat`

Send a message and get an AI reply.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-Lyzr-Api-Key: your-lyzr-key" \
  -d '{
    "merchant_id": "merchant_001",
    "sender": "+919876543210",
    "message": "What cakes do you have?"
  }'
```

**Headers**

| Header | Required | Description |
|--------|----------|-------------|
| `X-Lyzr-Api-Key` | Yes* | Lyzr API key. Not required if `LYZR_API_KEY` is set in env. |
| `X-Lyzr-Agent-Id` | No | Reuse an existing Lyzr agent ID. Leave blank to auto-create. |

**Response**

```json
{
  "session_id": "merchant_001:+919876543210",
  "reply": "Namaste! Humare paas Chocolate Cake (₹500), Vanilla Cake (₹400)..."
}
```

---

## Development

```bash
cd service

# Run tests
make test

# Lint
make lint

# Format
make fmt
```

---

## Mock Merchants

Two merchants are pre-loaded for demo/testing:

| ID | Name | Catalog |
|----|------|---------|
| `merchant_001` | Amit's Cake Shop | Chocolate, Vanilla, Red Velvet cakes |
| `merchant_002` | Priya's Thali House | Veg & Non-veg thali |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Agent | [Lyzr Agent Studio](https://studio.lyzr.ai) (Claude Sonnet 4.5) |
| Backend | FastAPI + Uvicorn |
| Demo UI | Streamlit |
| Database (planned) | Supabase Postgres |
| Payments (planned) | Razorpay Route |
| Messaging (planned) | WhatsApp Cloud API |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LYZR_API_KEY` | `""` | Lyzr API key. Can be passed per-request via header instead. |
| `COMVERSE_AGENT_ID` | `""` | Existing Lyzr agent ID. Leave blank to auto-create on first use. |
