import os
import json
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

# Load project-level environment selector
load_dotenv(BASE_DIR / ".env")

APP_ENV = os.getenv("APP_ENV", "dev")

# Load environment-specific configuration
ENV_FILE = BASE_DIR / "env" / f".env.{APP_ENV}"

if not ENV_FILE.exists():
    raise RuntimeError(f"Environment file not found: {ENV_FILE}")

load_dotenv(ENV_FILE, override=True)

# DATABASE

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://"
    f"{quote_plus(POSTGRES_USER or '')}:"
    f"{quote_plus(POSTGRES_PASSWORD or '')}@"
    f"localhost:5432/"
    f"{POSTGRES_DB}"
)


# REDIS

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


# RATE LIMIT

RATE_LIMIT = int(os.getenv("RATE_LIMIT", "10"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

# CACHE

JOBS_CACHE_TTL = int(os.getenv("JOBS_CACHE_TTL", "900"))

# AI

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# OAUTH

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# AIRTABLE
ALLOWED_JOB_FIELDS = set(json.loads(os.getenv("ALLOWED_JOB_FIELDS", "[]")))
JOB_LOOKBACK_DAYS = int(os.getenv("JOB_LOOKBACK_DAYS", "90"))
MAX_JOB_EXPERIENCE = int(os.getenv("MAX_JOB_EXPERIENCE", "5"))
