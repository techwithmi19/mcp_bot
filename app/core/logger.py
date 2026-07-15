import logging
import sys


class Logger:
    """
    Centralized application logger.
    """

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger:
            return cls._logger

        logger = logging.getLogger("mcp-chat")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        logger.propagate = False

        cls._logger = logger

        return logger


logger = Logger.get_logger()