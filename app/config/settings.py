# from dotenv import load_dotenv
# import os

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MCP_SERVER_URL = "http://172.20.26.168:8000/mcp"

# MODEL_NAME = "gpt-4.1"

# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY is not set.")


from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MCP_SERVER_URL = os.getenv(
    "MCP_SERVER_URL",
    "http://172.20.26.168:8000/mcp",
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-4.1",
)