import asyncio

from app.services.mcp_service import MCPService


SERVER_URL = "http://172.20.26.168:8000/mcp"


async def main():

    mcp = MCPService(SERVER_URL)

    await mcp.connect()

    tools = await mcp.list_tools()

    print(tools)

    await mcp.disconnect()


if __name__ == "__main__":
    asyncio.run(main())