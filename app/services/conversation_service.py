from app.models.conversation import ConversationMessage


class ConversationService:
    """
    Service responsible for maintaining conversation history.
    """

    def __init__(self):
        self.messages: list = []

    def clear(self) -> None:
        """
        Clear the current conversation.
        """
        self.messages.clear()

    def add_system_message(self, content: str) -> None:
        """
        Add a system message.
        """
        self.messages.append(
            ConversationMessage(
                role="system",
                content=content,
            ).model_dump()
        )

    def add_user_message(self, content: str) -> None:
        """
        Add a user message.
        """
        self.messages.append(
            ConversationMessage(
                role="user",
                content=content,
            ).model_dump()
        )

    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant message.
        """
        self.messages.append(
            ConversationMessage(
                role="assistant",
                content=content,
            ).model_dump()
        )

    def add_tool_message(
        self,
        tool_call_id: str,
        content: str,
    ) -> None:
        """
        Add a tool response message.
        """
        self.messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content,
            }
        )

    def add_tool_call_message(self, assistant_message) -> None:
        """
        Add the assistant message that contains tool calls.
        """
        self.messages.append(assistant_message.model_dump())

    def get_messages(self) -> list:
        """
        Return the complete conversation history.
        """
        return self.messages

    def get_last_message(self):
        """
        Return the last message in the conversation.
        """
        if not self.messages:
            return None

        return self.messages[-1]