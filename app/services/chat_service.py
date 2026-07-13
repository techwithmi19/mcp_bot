from app.services.conversation_service import ConversationService
from pprint import pprint


class ChatService:

    def __init__(self, llm_service, mcp_service):
        self.llm_service = llm_service
        self.mcp_service = mcp_service
        self.conversation_service = ConversationService()

    async def chat(self, message: str) -> str:
        """
        Process a user message and return the assistant response.
        """

        # Store user message
        self.conversation_service.add_user_message(message)

        # Get MCP tools
        tools = await self.mcp_service.list_tools()

        # Ask LLM
        response = self.llm_service.ask(
            self.conversation_service.get_messages(),
            tools,
        )

        assistant_message = response.choices[0].message

        # print("\n========== Assistant Message ==========")
        # pprint(assistant_message.model_dump())
        # print("=======================================\n")

        # No tool required
        if not assistant_message.tool_calls:

            self.conversation_service.add_assistant_message(
                assistant_message.content
            )

            return assistant_message.content

        # Save assistant tool call
        self.conversation_service.add_tool_call_message(
            assistant_message
        )

        # Execute first tool
        for tool_call in assistant_message.tool_calls:

            tool_response = await self.mcp_service.execute_tool(
                tool_call.function.name,
                tool_call.function.arguments,
            )

            self.conversation_service.add_tool_message(
                tool_call.id,
                tool_response.content[0].text,
            )

        print("\n========== Conversation ==========")
        pprint(self.conversation_service.get_messages())
        print("==================================\n")

        # Ask LLM again with updated conversation
        final_response = self.llm_service.generate_final_answer(
            self.conversation_service.get_messages(),
            tools,
        )

        

        final_answer = final_response.choices[0].message.content

        # Save assistant response
        self.conversation_service.add_assistant_message(
            final_answer
        )

        return final_answer