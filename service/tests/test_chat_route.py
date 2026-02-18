def test_chat_returns_reply(client, mock_agent):
    response = client.post("/chat", json={
        "merchant_id": "merchant_001",
        "sender": "+919876543210",
        "message": "Show me your cakes",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "Sure! We have Chocolate (₹500) and Vanilla (₹400)."
    assert data["session_id"] == "merchant_001:+919876543210"


def test_chat_uses_correct_session_id(client, mock_agent):
    client.post("/chat", json={
        "merchant_id": "merchant_002",
        "sender": "+911234567890",
        "message": "What thalis do you have?",
    })

    # Agent is called with enriched message (includes catalog context) and correct session_id
    mock_agent.run.assert_called_once()
    _, kwargs = mock_agent.run.call_args
    assert kwargs["session_id"] == "merchant_002:+911234567890"


def test_chat_unknown_merchant_returns_404(client):
    response = client.post("/chat", json={
        "merchant_id": "ghost_merchant",
        "sender": "+919999999999",
        "message": "Hello",
    })

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_chat_missing_fields_returns_422(client):
    response = client.post("/chat", json={"merchant_id": "merchant_001"})
    assert response.status_code == 422
