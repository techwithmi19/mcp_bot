from app.core.llm.openai_client import client
from app.config.settings import MODEL_NAME


class LLMService:

    def ask(self, message, tools):

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

        return client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )