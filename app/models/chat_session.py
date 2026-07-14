from datetime import datetime

from app.services.conversation_service import ConversationService


class ChatSession:
    """
    Represents a single user chat session.
    """

    def __init__(self):
        self.conversation = ConversationService()
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()

    def touch(self):
        """
        Update the last accessed timestamp.
        """
        self.last_accessed = datetime.now()