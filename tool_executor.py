import json


async def execute_tool(session, tool_call):

    tool_name = tool_call.function.name

    arguments = json.loads(
        tool_call.function.arguments
    )

    result = await session.call_tool(
        tool_name,
        arguments
    )

    return result