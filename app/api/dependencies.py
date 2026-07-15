from app.bootstrap.container import container
from app.services.chat_service import ChatService


def get_chat_service() -> ChatService:
    """
    Returns the application ChatService.
    """

    return container.chat_service