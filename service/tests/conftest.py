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
