from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings
from routes.chat import router
from services.lyzr import init_lyzr


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Per-request agent cache keyed by api_key
    app.state.agents_cache = {}

    # If env key is configured, pre-warm the default agent
    if settings.lyzr_api_key:
        app.state.agent = init_lyzr(
            api_key=settings.lyzr_api_key,
            agent_id=settings.comverse_agent_id,
        )

    yield


app = FastAPI(title="Comverse Service", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
