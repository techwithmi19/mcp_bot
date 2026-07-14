class ToolRegistry:
    """
    Maintains a cached list of MCP tools.

    The registry loads the tools once when the application starts
    and serves them from memory for all future requests.
    """

    def __init__(self, mcp_service):
        self.mcp_service = mcp_service
        self._tools = []

    async def initialize(self):
        """
        Load all MCP tools and cache them.
        """

        self._tools = await self.mcp_service.list_tools()
        print(f"Loaded {len(self._tools)} MCP tools.")
        

    def get_tools(self):
        """
        Return cached tools.
        """

        return self._tools

    async def refresh(self):
        """
        Reload tools from MCP server.
        """

        await self.initialize()