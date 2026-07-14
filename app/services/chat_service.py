from app.services.conversation_service import ConversationService
from app.services.prompt_service import PromptService


class ChatService:

    def __init__(self, llm_service, mcp_service, tool_registry):
        self.llm_service = llm_service
        self.mcp_service = mcp_service
        self.tool_registry = tool_registry

        self.conversation_service = ConversationService()
        self.prompt_service = PromptService()


    async def chat(self, message: str) -> str:
        """
        Process a user message and return the assistant response.
        """

        # Store user message
        self.conversation_service.add_user_message(message)

        # Get available tools
        tools = self.tool_registry.get_tools()

        # Build prompt
        messages = self.prompt_service.build_messages(
            self.conversation_service.get_messages()
        )

        # Ask LLM
        response = self.llm_service.ask(
            messages,
            tools,
        )

        assistant_message = response.choices[0].message

        # No tool required
        if not assistant_message.tool_calls:

            self.conversation_service.add_assistant_message(
                assistant_message.content
            )

            return assistant_message.content

        # Store assistant tool calls
        self.conversation_service.add_tool_call_message(
            assistant_message
        )

        # Execute all requested tools
        for tool_call in assistant_message.tool_calls:

            tool_response = await self.mcp_service.execute_tool(
                tool_call.function.name,
                tool_call.function.arguments,
            )

            self.conversation_service.add_tool_message(
                tool_call.id,
                tool_response.content[0].text,
            )

        # Build updated prompt
        messages = self.prompt_service.build_messages(
            self.conversation_service.get_messages()
        )

        # Generate final answer
        final_response = self.llm_service.generate_final_answer(
            messages,
            tools,
        )

        final_answer = final_response.choices[0].message.content

        self.conversation_service.add_assistant_message(
            final_answer
        )

        return final_answer