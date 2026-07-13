class CLI:

    def __init__(self, chat_service):
        self.chat_service = chat_service

    async def start(self):

        print("=" * 60)
        print("        GitLab AI Assistant")
        print("=" * 60)
        print("Type 'exit' to quit.\n")

        while True:

            message = input("You: ").strip()

            if message.lower() in ("exit", "quit"):
                print("\nGoodbye!")
                break

            if not message:
                continue

            try:
                answer = await self.chat_service.chat(message)

                print("\nAssistant:")
                print(answer)
                print()

            except Exception as ex:
                print(f"\nError: {ex}\n")