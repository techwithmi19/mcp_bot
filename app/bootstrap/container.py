from app.config.settings import MCP_SERVER_URL
from app.core.logger import logger

from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.mcp_service import MCPService
from app.services.session_manager import SessionManager
from app.services.tool_registry import ToolRegistry

from app.services.configuration_service import ConfigurationService


class Container:
    """
    Creates and manages application services.
    """

    def __init__(self):
        self._mcp_service: MCPService | None = None
        self._tool_registry: ToolRegistry | None = None
        self._session_manager: SessionManager | None = None
        self._llm_service: LLMService | None = None
        self._chat_service: ChatService | None = None

    @property
    def mcp_service(self) -> MCPService:
        return self._mcp_service

    @property
    def tool_registry(self) -> ToolRegistry:
        return self._tool_registry

    @property
    def session_manager(self) -> SessionManager:
        return self._session_manager

    @property
    def llm_service(self) -> LLMService:
        return self._llm_service

    @property
    def chat_service(self) -> ChatService:
        return self._chat_service

    async def initialize(self):
        """
        Initialize all application services.
        """
        try:
            logger.info(f"Connecting to MCP Server: {MCP_SERVER_URL}")

            ConfigurationService.validate()

            self._mcp_service = MCPService(MCP_SERVER_URL)
            await self._mcp_service.connect()

            self._tool_registry = ToolRegistry(
                self._mcp_service
            )
            await self._tool_registry.initialize()

            logger.info(
                f"Loaded {len(self._tool_registry.get_tools())} MCP tools."
            )

            self._session_manager = SessionManager()

            self._llm_service = LLMService()

            self._chat_service = ChatService(
                llm_service=self._llm_service,
                mcp_service=self._mcp_service,
                tool_registry=self._tool_registry,
                session_manager=self._session_manager,
            )

            logger.info("Application initialized successfully.")

        except Exception:
            logger.error(
                "Failed to initialize application services."
            )
            raise

    async def shutdown(self):
        """
        Shutdown application services.
        """
        try:
            logger.info("Shutting down application.")

            if self._mcp_service:
                await self._mcp_service.disconnect()

        except Exception:

            logger.exception(
                "Error during shutdown."
            )

            raise

        logger.info("Application shutdown completed.")

# Global application container
container = Container()        