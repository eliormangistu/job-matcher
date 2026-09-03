import os

from dotenv import load_dotenv

load_dotenv()


# DATABASE

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://"
    f"{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"localhost:5432/"
    f"{POSTGRES_DB}"
)


# REDIS

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


# RATE LIMIT

RATE_LIMIT = int(os.getenv("RATE_LIMIT", "10"))
RATE_LIMIT_WINDOW_SECONDS = int(
    os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")
)

# CACHE

JOBS_CACHE_TTL = int(
    os.getenv("JOBS_CACHE_TTL", "900")
)