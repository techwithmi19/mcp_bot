from llm_client import client
from config import MODEL_NAME


class ChatService:

    def __init__(self, session):
        self.session = session

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