class ToolExecutor:

    def __init__(self, session):
        self.session = session

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):
        return await self.session.call_tool(
            tool_name,
            arguments,
        )