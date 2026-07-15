from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """
    Process a chat request.
    """

    response = await chat_service.chat(
        session_id=request.session_id,
        message=request.message,
    )

    return ChatResponse(
        response=response,
    )