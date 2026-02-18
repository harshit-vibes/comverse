from unittest.mock import MagicMock
from services.lyzr import run_agent


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
