from app.core.llm.openai_client import client
from app.config.settings import MODEL_NAME


class LLMService:
    """
    Service responsible for communicating with the LLM.
    """

    def ask(
        self,
        messages: list,
        tools: list,
    ):

        return client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )

    def generate_final_answer(
        self,
        messages: list,
        tools: list,
    ):

        return client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )