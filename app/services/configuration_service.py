from app.config import settings
from app.core.exceptions import ConfigurationError
from app.core.logger import logger


class ConfigurationService:
    """
    Validates application configuration.
    """

    @staticmethod
    def validate():

        logger.info("Validating configuration...")

        required_settings = {
            "OPENAI_API_KEY": settings.OPENAI_API_KEY,
            "MCP_SERVER_URL": settings.MCP_SERVER_URL,
            "MODEL_NAME": settings.MODEL_NAME,
        }

        missing = [
            key
            for key, value in required_settings.items()
            if not value
        ]

        if missing:
            raise ConfigurationError(
                "Missing required configuration: "
                + ", ".join(missing)
            )

        logger.info("Configuration validation successful.")