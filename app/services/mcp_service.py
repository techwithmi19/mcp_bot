from app.core.mcp.mcp_client import MCPClient
from app.core.mcp.tool_executor import ToolExecutor

class MCPService:
    """
    Service responsible for interacting with MCP server.
    """

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.client = MCPClient(server_url)
        self.session = None
        self.tool_executor = None

    async def connect(self):
        """
        Create MCP session
        """

        self.session = await self.client.connect()
        self.tool_executor = ToolExecutor(self.session)
        

    async def disconnect(self):
        """
        Close MCP session
        """

        if self.client:
            await self.client.close()

    
    async def list_tools(self):
        """
        Return MCP tools formatted for OpenAI.
        """
        result = await self.session.list_tools()

        tools = []

        for tool in result.tools:
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
            )

        return tools
    
    
    async def execute_tool(self, tool_call):
        if self.tool_executor is None:
            raise RuntimeError(
                "MCP is not connected. Call connect() first."
            )

        return await self.tool_executor.execute_tool(tool_call)
