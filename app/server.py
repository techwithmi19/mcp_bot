import asyncio

from app.config.settings import MCP_SERVER_URL
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.mcp_service import MCPService


def run():
    asyncio.run(start())


async def start():

    mcp_service = MCPService(MCP_SERVER_URL)

    llm_service = LLMService()

    chat = ChatService(
        mcp_service=mcp_service,
        llm_service=llm_service,
    )

    await chat.start()