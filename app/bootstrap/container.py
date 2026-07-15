from app.config.settings import MCP_SERVER_URL

from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.mcp_service import MCPService
from app.services.session_manager import SessionManager
from app.services.tool_registry import ToolRegistry
from app.core.logger import logger


class Container:
    """
    Creates and manages application services.
    """

    def __init__(self):
        self.mcp_service = None
        self.tool_registry = None
        self.session_manager = None
        self.llm_service = None
        self.chat_service = None

    async def initialize(self):
        """
        Initialize all application services.
        """

        # MCP
        self.mcp_service = MCPService(MCP_SERVER_URL)
        await self.mcp_service.connect()
        logger.info(f"Connecting to MCP Server: {MCP_SERVER_URL}")

        # Tool Registry
        self.tool_registry = ToolRegistry(
            self.mcp_service
        )
        await self.tool_registry.initialize()

        # Session Manager
        self.session_manager = SessionManager()

        # LLM
        self.llm_service = LLMService()

        # Chat
        self.chat_service = ChatService(
            llm_service=self.llm_service,
            mcp_service=self.mcp_service,
            tool_registry=self.tool_registry,
            session_manager=self.session_manager,
        )

    async def shutdown(self):
        """
        Shutdown application services.
        """

        if self.mcp_service:
            await self.mcp_service.disconnect()