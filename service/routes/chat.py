from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from models.chat import ChatRequest, ChatResponse
from mocks.merchants import get_merchant
from services.lyzr import init_lyzr, run_agent

router = APIRouter()


def get_agent(
    req: Request,
    x_lyzr_api_key: Optional[str] = Header(default=None),
    x_lyzr_agent_id: Optional[str] = Header(default=None),
):
    """Resolve the Lyzr agent for this request.

    Priority:
    1. X-Lyzr-Api-Key + X-Lyzr-Agent-Id headers — fetches and caches that agent
    2. app.state.agent                            — pre-warmed at startup via env config
    3. 4xx                                        — missing credentials
    """
    if x_lyzr_api_key:
        if not x_lyzr_agent_id:
            raise HTTPException(
                status_code=400,
                detail="X-Lyzr-Agent-Id header is required.",
            )
        cache = req.app.state.agents_cache
        cache_key = f"{x_lyzr_api_key}:{x_lyzr_agent_id}"
        if cache_key not in cache:
            cache[cache_key] = init_lyzr(
                api_key=x_lyzr_api_key,
                agent_id=x_lyzr_agent_id,
            )
        return cache[cache_key]

    if hasattr(req.app.state, "agent"):
        return req.app.state.agent

    raise HTTPException(
        status_code=503,
        detail="Lyzr credentials not configured. Provide X-Lyzr-Api-Key and X-Lyzr-Agent-Id headers.",
    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, agent=Depends(get_agent)):
    merchant = get_merchant(request.merchant_id)
    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail=f"Merchant '{request.merchant_id}' not found",
        )

    session_id = f"{merchant.id}:{request.sender}"

    # Inject merchant catalog so the agent always has product context
    message_with_context = (
        f"[Merchant: {merchant.name} | Catalog: {merchant.catalog_summary}]\n"
        f"{request.message}"
    )
    reply = run_agent(agent=agent, message=message_with_context, session_id=session_id)
    return ChatResponse(session_id=session_id, reply=reply)
