import os
from lyzr import Studio


def init_lyzr(api_key: str, agent_id: str):
    """Initialize Lyzr agent by fetching an existing agent. Agent ID is mandatory."""
    os.environ["LYZR_API_KEY"] = api_key
    return Studio().get_agent(agent_id)


def run_agent(agent, message: str, session_id: str) -> str:
    """Send a message to the agent and return the text response."""
    response = agent.run(message, session_id=session_id)
    return response.response
