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
    1. X-Lyzr-Api-Key header  — creates/caches an agent for that key
    2. app.state.agent         — pre-warmed at startup via env config
    3. 503                     — no key available anywhere
    """
    if x_lyzr_api_key:
        cache = req.app.state.agents_cache
        if x_lyzr_api_key not in cache:
            cache[x_lyzr_api_key] = init_lyzr(
                api_key=x_lyzr_api_key,
                agent_id=x_lyzr_agent_id or "",
            )
        return cache[x_lyzr_api_key]

    if hasattr(req.app.state, "agent"):
        return req.app.state.agent

    raise HTTPException(
        status_code=503,
        detail="Lyzr API key not configured. Provide the X-Lyzr-Api-Key header.",
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
