from app.core.logger import logger

class CLI:

    def __init__(self, chat_service):
        self.chat_service = chat_service

    async def start(self):

        logger.info("=" * 60)
        logger.info("        GitLab AI Assistant")
        logger.info("=" * 60)
        logger.info("Type 'exit' to quit.\n")

        while True:

            message = input("You: ").strip()

            if message.lower() in ("exit", "quit"):
                logger.info("\nGoodbye!")
                break

            if not message:
                continue

            try:
                answer = await self.chat_service.chat(message)

                logger.info("\nAssistant:")
                logger.info(answer)
                logger.info()

            except Exception as ex:
                logger.info(f"\nError: {ex}\n")