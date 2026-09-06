import os
from urllib.parse import quote_plus

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

RATE_LIMIT = 1000
RATE_LIMIT_WINDOW_SECONDS = 60

# CACHE

JOBS_CACHE_TTL = 900

# AI

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# OAUTH

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# AIRTABLE
JOB_LOOKBACK_DAYS = 90
MAX_JOB_EXPERIENCE = 5
ALLOWED_JOB_FIELDS = [
    "Software Engineering",
    "Data Science, ML & Algorithms",
    "DevOps",
    "Data Engineering",
    "Frontend Development",
    "Mobile Development",
    "Embedded, Low Level & Firmware Engineering",
]

# JOB
SKILL_WEIGHT = 50
EXPERIENCE_WEIGHT = 20
ROLE_WEIGHT = 15
LANGUAGE_WEIGHT = 10
EDUCATION_WEIGHT = 5
