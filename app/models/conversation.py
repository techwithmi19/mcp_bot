from app.models.common import BaseSchema


class ConversationMessage(BaseSchema):
    role: str
    content: str