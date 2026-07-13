import asyncio

from app.config.settings import MCP_SERVER_URL
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.mcp_service import MCPService
from app.cli import CLI


def run():
    asyncio.run(start())


async def start():

    # Create services
    mcp_service = MCPService(MCP_SERVER_URL)
    llm_service = LLMService()

    # Connect to MCP
    await mcp_service.connect()

    try:
        # Create Chat Service
        chat_service = ChatService(
            llm_service,
            mcp_service,
        )

        # Start CLI
        cli = CLI(chat_service)

        await cli.start()

    finally:
        await mcp_service.disconnect()