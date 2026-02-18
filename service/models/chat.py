from pydantic import BaseModel


class ChatRequest(BaseModel):
    merchant_id: str
    sender: str   # customer phone number
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
