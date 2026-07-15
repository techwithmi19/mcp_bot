from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """
    Chat response returned to the client.
    """

    response: str = Field(
        ...,
        description="Assistant response.",
    )