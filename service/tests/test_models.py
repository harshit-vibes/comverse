import pytest
from pydantic import ValidationError
from models.chat import ChatRequest, ChatResponse


def test_chat_request_valid():
    req = ChatRequest(merchant_id="merchant_001", sender="+919876543210", message="Hi")
    assert req.merchant_id == "merchant_001"
    assert req.sender == "+919876543210"
    assert req.message == "Hi"


def test_chat_request_requires_all_fields():
    with pytest.raises(ValidationError):
        ChatRequest(merchant_id="merchant_001")  # missing sender + message


def test_chat_response_valid():
    resp = ChatResponse(session_id="merchant_001:+919876543210", reply="Hello!")
    assert resp.session_id == "merchant_001:+919876543210"
    assert resp.reply == "Hello!"
