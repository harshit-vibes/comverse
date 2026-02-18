import pytest
from config import Settings


def test_settings_loads_from_env(monkeypatch):
    monkeypatch.setenv("LYZR_API_KEY", "test-key-123")
    monkeypatch.setenv("COMVERSE_AGENT_ID", "agent-abc")

    settings = Settings()

    assert settings.lyzr_api_key == "test-key-123"
    assert settings.comverse_agent_id == "agent-abc"


def test_settings_api_key_defaults_to_empty(monkeypatch):
    monkeypatch.delenv("LYZR_API_KEY", raising=False)
    monkeypatch.delenv("COMVERSE_AGENT_ID", raising=False)

    settings = Settings(_env_file=None)  # bypass .env file
    assert settings.lyzr_api_key == ""


def test_agent_id_defaults_to_empty(monkeypatch):
    monkeypatch.setenv("LYZR_API_KEY", "test-key")
    monkeypatch.delenv("COMVERSE_AGENT_ID", raising=False)

    settings = Settings()
    assert settings.comverse_agent_id == ""
