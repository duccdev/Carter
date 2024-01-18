from os import getenv
from dotenv import load_dotenv
import logger

load_dotenv()

TOKEN = getenv("TOKEN", "")
CAT_API = getenv("CAT_API", "")
GENAI = getenv("GENAI", "")
PGSQL = getenv("PGSQL", "")
CARTER_ENV = getenv("CARTER_ENV", "")

if not TOKEN or not CAT_API or not GENAI or not PGSQL or not CARTER_ENV:
    logger.error("Invalid .env, please consult .env.example and the readme")
    exit(1)

BOT_PREFIX = "c."
