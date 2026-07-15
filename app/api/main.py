from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bootstrap.container import container
from app.core.logger import logger
from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown.
    """

    logger.info("Starting FastAPI application...")

    await container.initialize()

    yield

    logger.info("Stopping FastAPI application...")

    await container.shutdown()


app = FastAPI(
    title="MCP Chat API",
    description="REST API for interacting with MCP servers using OpenAI tool calling.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(chat_router)