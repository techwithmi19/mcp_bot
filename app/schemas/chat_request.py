from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request received from the client.
    """

    session_id: str = Field(
        ...,
        description="Unique session identifier.",
        examples=["user-123"],
    )

    message: str = Field(
        ...,
        description="User message.",
        examples=["Show MR details for project 28 and MR 6746"],
    )