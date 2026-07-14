import asyncio

from app.config.settings import MCP_SERVER_URL
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.mcp_service import MCPService
from app.services.session_manager import SessionManager
from app.services.tool_registry import ToolRegistry


def run():
    asyncio.run(start())


async def start():
    # Initialize MCP Service
    mcp_service = MCPService(MCP_SERVER_URL)
    await mcp_service.connect()

    # Cache all MCP tools
    tool_registry = ToolRegistry(mcp_service)
    await tool_registry.initialize()

    # Create Session Manager
    session_manager = SessionManager()

    # Initialize LLM Service
    llm_service = LLMService()

    # Initialize Chat Service
    chat_service = ChatService(
        llm_service=llm_service,
        mcp_service=mcp_service,
        tool_registry=tool_registry,
        session_manager=session_manager,
    )

    print("Chat application started.")
    print("Type 'exit' to quit.\n")

    try:
        while True:
            message = input("You: ")

            if message.lower() in ["exit", "quit"]:
                break

            # session = input("Session: ")
            response = await chat_service.chat(
                session_id="console",
                message=message,
            )

            print(session_manager.get_active_sessions().keys())
            print(f"\nAssistant: {response}\n")

    finally:
        await mcp_service.disconnect()