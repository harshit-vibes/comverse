import os
from lyzr import Studio


def init_lyzr(api_key: str, agent_id: str = ""):
    """Initialize Lyzr agent. Retrieves existing agent if agent_id provided,
    otherwise creates a new one. Called once at app startup."""
    os.environ["LYZR_API_KEY"] = api_key
    studio = Studio()

    if agent_id:
        return studio.get_agent(agent_id)

    return studio.create_agent(
        name="Comverse Ordering Agent",
        provider="anthropic/claude-sonnet-4-5",
        role="WhatsApp commerce assistant for Indian SMBs",
        goal="Help customers browse catalog, place orders, and answer questions in Hinglish",
        instructions=(
            "Respond in Hinglish (mix of Hindi and English). "
            "Be warm, concise, and helpful. "
            "Guide customers through ordering step by step. "
            "Always reference the merchant's catalog when answering product questions."
        ),
    )


def run_agent(agent, message: str, session_id: str) -> str:
    """Send a message to the agent and return the text response."""
    response = agent.run(message, session_id=session_id)
    return response.response
