class ApplicationError(Exception):
    """
    Base class for all application exceptions.
    """


class ConfigurationError(ApplicationError):
    """
    Raised when application configuration is invalid.
    """


class MCPConnectionError(ApplicationError):
    """
    Raised when MCP server connection fails.
    """


class MCPToolExecutionError(ApplicationError):
    """
    Raised when an MCP tool execution fails.
    """


class LLMError(ApplicationError):
    """
    Raised when an LLM request fails.
    """


class SessionNotFoundError(ApplicationError):
    """
    Raised when a chat session cannot be found.
    """