from app.models.common import BaseSchema


class ChatRequest(BaseSchema):
    message: str


class ChatResponse(BaseSchema):
    answer: str