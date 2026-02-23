from contextlib import asynccontextmanager
from typing import Optional
import httpx
from fastapi import FastAPI, Header, HTTPException
from config import settings
from routes.chat import router
from services.lyzr import init_lyzr

LYZR_AGENT_API = "https://agent-prod.studio.lyzr.ai"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Per-request agent cache keyed by api_key
    app.state.agents_cache = {}

    # Pre-warm the default agent — both key and agent ID are required
    if settings.lyzr_api_key and settings.comverse_agent_id:
        app.state.agent = init_lyzr(
            api_key=settings.lyzr_api_key,
            agent_id=settings.comverse_agent_id,
        )
    elif settings.lyzr_api_key or settings.comverse_agent_id:
        raise RuntimeError(
            "Both LYZR_API_KEY and COMVERSE_AGENT_ID must be set together in .env"
        )

    yield


app = FastAPI(title="Comverse Service", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/validate")
def validate_key(
    x_lyzr_api_key: Optional[str] = Header(default=None),
    x_lyzr_agent_id: Optional[str] = Header(default=None),
):
    """Validate credentials with a direct HTTP call — bypasses SDK retries for fast response."""
    if not x_lyzr_api_key:
        raise HTTPException(status_code=400, detail="X-Lyzr-Api-Key header required")
    if not x_lyzr_agent_id:
        raise HTTPException(status_code=400, detail="X-Lyzr-Agent-Id header required")
    try:
        resp = httpx.get(
            f"{LYZR_AGENT_API}/v3/agents/{x_lyzr_agent_id}",
            headers={"x-api-key": x_lyzr_api_key},
            timeout=5,
        )
        if resp.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Agent not found. Check the Agent ID.")
        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail="Lyzr API error.")
        return {"valid": True}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Lyzr API did not respond in time.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


