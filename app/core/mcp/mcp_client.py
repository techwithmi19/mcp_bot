from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


class MCPClient:

    def __init__(self, server_url):
        self.server_url = server_url
        print(f"Connecting to: {self.server_url}")

    async def connect(self):

        self.transport = streamablehttp_client(self.server_url)

        (
            self.read_stream,
            self.write_stream,
            _,
        ) = await self.transport.__aenter__()

        self.session = ClientSession(
            self.read_stream,
            self.write_stream
        )

        await self.session.__aenter__()

        await self.session.initialize()

        return self.session

    async def close(self):
        await self.session.__aexit__(None, None, None)
        await self.transport.__aexit__(None, None, None)