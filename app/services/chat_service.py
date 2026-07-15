from app.core.logger import logger
from app.services.prompt_service import PromptService


class ChatService:

    def __init__(
        self,
        llm_service,
        mcp_service,
        tool_registry,
        session_manager,
    ):
        self.llm_service = llm_service
        self.mcp_service = mcp_service
        self.tool_registry = tool_registry
        self.session_manager = session_manager
        self.prompt_service = PromptService()

    async def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:
        """
        Process a user message and return the assistant response.
        """

        # Get the user's session
        session = self.session_manager.get_session(session_id)

        # Get conversation for this session
        conversation = session.conversation

        # Store user message
        conversation.add_user_message(message)

        # Get cached MCP tools
        tools = self.tool_registry.get_tools()

        # Build messages
        messages = self.prompt_service.build_messages(
            conversation.get_messages()
        )

        # Ask LLM
        response = self.llm_service.ask(
            messages,
            tools,
        )

        assistant_message = response.choices[0].message

        # No tool call required
        if not assistant_message.tool_calls:

            conversation.add_assistant_message(
                assistant_message.content
            )

            return assistant_message.content

        # Save assistant tool call
        conversation.add_tool_call_message(
            assistant_message
        )

        # Execute first tool call
        logger.info(f"Tool calls received: {len(assistant_message.tool_calls)}")
        # tool_call = assistant_message.tool_calls[0]
        for tool_call in assistant_message.tool_calls:

            tool_response = await self.mcp_service.execute_tool(
                tool_call.function.name,
                tool_call.function.arguments,
            )

            # Save tool response
            conversation.add_tool_message(
                tool_call.id,
                str(tool_response.content),
            )

        # Build updated conversation
        messages = self.prompt_service.build_messages(
            conversation.get_messages()
        )

        # --------------------------------------------------
        # Temporary Debugging (Remove after issue is resolved)
        # --------------------------------------------------

        assistant_tool_calls = 0
        tool_responses = 0

        for msg in messages:

            if (
                msg["role"] == "assistant"
                and msg.get("tool_calls")
            ):
                assistant_tool_calls += len(msg["tool_calls"])

            elif msg["role"] == "tool":
                tool_responses += 1

        if assistant_tool_calls != tool_responses:

            from pprint import pprint

            print("\n" + "=" * 80)
            print("Conversation Mismatch Detected")
            print("=" * 80)

            pprint(messages)

            print("\nAssistant Tool Calls :", assistant_tool_calls)
            print("Tool Responses       :", tool_responses)

            print("=" * 80 + "\n")

        # --------------------------------------------------
        # End Debugging
        # --------------------------------------------------

        # Generate final response
        final_response = self.llm_service.generate_final_answer(
            messages,
            tools,
        )

        final_answer = final_response.choices[0].message.content

        # Save assistant response
        conversation.add_assistant_message(
            final_answer
        )

        return final_answer