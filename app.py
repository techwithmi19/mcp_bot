import asyncio

from config import MCP_SERVER_URL
from mcp_client import MCPClient
from chat_service import ChatService
from tool_executor import execute_tool


async def main():

    mcp = MCPClient(MCP_SERVER_URL)

    session = await mcp.connect()

    chat = ChatService(session)

    tools = await chat.get_tools()

    question = "Show changed files for project ID 52607 and merge request ID 1."

    response = chat.ask_llm(question, tools)

    if response.choices[0].message.tool_calls:

        tool_call = response.choices[0].message.tool_calls[0]

        tool_result = await execute_tool(
            session,
            tool_call,
        )

        final = chat.generate_final_answer(
            question,
            tool_result,
            tool_call,
            response,
            tools,
        )

        print(final.choices[0].message.content)

    else:

        print(response.choices[0].message.content)

    await mcp.close()


if __name__ == "__main__":
    asyncio.run(main())