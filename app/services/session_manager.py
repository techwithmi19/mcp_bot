from app.models.chat_session import ChatSession
from app.core.exceptions import SessionNotFoundError


class SessionManager:
    """
    Responsible for managing all active chat sessions.
    """

    def __init__(self):
        self._sessions = {}

    def get_session(self, session_id: str) -> ChatSession:
        """
        Return an existing session or create a new one.
        """
        try:
            
            if session_id not in self._sessions:
                self._sessions[session_id] = ChatSession()

            session = self._sessions[session_id]
            session.touch()

            return session
        
        except Exception as ex:
            raise SessionNotFoundError(
                f"Session '{session_id}' not found."
            )

    def remove_session(self, session_id: str):
        """
        Remove a session.
        """

        self._sessions.pop(session_id, None)

    def clear(self):
        """
        Remove all sessions.
        """

        self._sessions.clear()

    def get_active_sessions(self):
        """
        Return all active sessions.
        """

        return self._sessions