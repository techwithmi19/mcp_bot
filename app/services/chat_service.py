from app.core.llm.openai_client import client
from app.config.settings import MODEL_NAME


class ChatService:

    def __init__(self, mcp_service, llm_service):
        self.mcp_service = mcp_service
        self.llm_service = llm_service


    async def start(self):

        await self.mcp_service.connect()

        while True:

            message = input("\nYou: ")

            if message.lower() in ("exit", "quit"):
                break

            await self.chat(message)

        await self.mcp_service.disconnect()


    async def chat(self, message):

        tools = await self.mcp_service.list_tools()

        response = self.llm_service.ask(
            message,
            tools,
        )

        assistant = response.choices[0].message

        if not assistant.tool_calls:
            print("\nAssistant:", assistant.content)
            return

        tool_call = assistant.tool_calls[0]

        tool_response = await self.mcp_service.execute_tool(
            tool_call
        )

        final = self.llm_service.generate_final_answer(
            message,
            tool_response,
            tool_call,
            response,
            tools,
        )

        print(
            "\nAssistant:",
            final.choices[0].message.content,
        )        

        
    async def get_tools(self):

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


    def ask_llm(self, message, tools):

        return client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            tools=tools,
        )


    def generate_final_answer(
        self,
        original_message,
        tool_response,
        tool_call,
        first_response,
        tools,
    ):

        messages = [
            {
                "role": "user",
                "content": original_message,
            },
            first_response.choices[0].message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_response.content),
            },
        ]

        final = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )

        return final