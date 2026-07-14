class PromptService:
    """
    Responsible for building prompts for the LLM.
    """

    def build_messages(self, conversation):
        """
        Build complete conversation including system prompt.
        """

        return [
            {
                "role": "system",
                "content": (
                    "You are an enterprise GitLab AI assistant.\n\n"
                    "Your responsibilities:\n"
                    "- Help users with GitLab repositories.\n"
                    "- Use MCP tools whenever information is required.\n"
                    "- Never hallucinate project or merge request information.\n"
                    "- If a required parameter is missing, ask the user for it.\n"
                    "- After receiving tool responses, summarize them clearly.\n"
                    "- Answer professionally and concisely."
                ),
            },
            *conversation,
        ]