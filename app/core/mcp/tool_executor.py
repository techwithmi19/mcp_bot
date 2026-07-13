import json


class ToolExecutor:

    def __init__(self, session):
        self.session = session

    async def execute_tool(self, tool_call):

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        return await self.session.call_tool(
            tool_name,
            arguments
        )