from os import getenv
from dotenv import load_dotenv
import logger

load_dotenv()

TOKEN = getenv("TOKEN", "")
CAT_API = getenv("CAT_API", "")
GENAI = getenv("GENAI", "")
SQLITE = getenv("SQLITE", "")
CARTER_ENV = getenv("CARTER_ENV", "prod")

if not TOKEN or not CAT_API or not GENAI or not SQLITE or not CARTER_ENV:
    logger.error("Invalid .env, please consult .env.example and the readme")
    exit(1)

BOT_PREFIX = "c." if CARTER_ENV == "prod" else "cd."
