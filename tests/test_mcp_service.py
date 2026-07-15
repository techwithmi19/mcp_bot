import asyncio

from app.services.mcp_service import MCPService
from app.core.logger import logger


SERVER_URL = "http://172.20.26.168:8000/mcp"


async def main():

    mcp = MCPService(SERVER_URL)

    await mcp.connect()

    tools = await mcp.list_tools()

    logger.info("Available MCP tools:")

    await mcp.disconnect()


if __name__ == "__main__":
    asyncio.run(main())