from app.core.llm.openai_client import client
from app.config.settings import MODEL_NAME
from app.core.exceptions import LLMError


class LLMService:
    """
    Service responsible for communicating with the LLM.
    """

    def ask(
        self,
        messages: list,
        tools: list,
    ):
        try:

            return client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
            )
        except Exception as ex:

            raise LLMError(
                "Failed to communicate with OpenAI."
            ) from ex
        

    def generate_final_answer(
        self,
        messages: list,
        tools: list,
    ):
        try:
            
            return client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
            )
        except Exception as ex:

            raise LLMError(
                "Failed to generate final response."
            ) from ex