import asyncio

from app.bootstrap.container import Container
from app.core.logger import logger


def run():
    asyncio.run(start())


async def start():

    container = Container()
    await container.initialize()

    chat_service = container.chat_service

    logger.info("Chat application started.")
    logger.info("Type 'exit' to quit.\n")

    try:

        while True:

            message = input("You: ")

            if message.lower() in ["exit", "quit"]:
                break

            try:
                response = await chat_service.chat(
                    session_id="console",
                    message=message,
                )
            except Exception as ex:

                logger.exception("Chat request failed.")

                print(f"\nError: {ex}\n")                                   

            logger.info(f"Assistant: {response}")

    finally:

        await container.shutdown()