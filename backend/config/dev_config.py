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

REDIS_URL = os.getenv("REDIS_URL")

# RATE LIMIT

RATE_LIMIT = 100
RATE_LIMIT_WINDOW_SECONDS = 60

# CACHE

JOBS_CACHE_TTL = 900

# AI

GEMINI_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]
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

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")

# AIRTABLE
AIRTABLE_VIEW_URL = (
    "https://airtable.com/embed/"
    "appwewqLk7iUY4azc/"
    "shrQBuWjXd0YgPqV6"
    "?backgroundColor=cyan&viewControls=on"
)

# CONTENT
SPACE_ID = os.getenv("SPACE_ID")
ENTRY_ID = os.getenv("ENTRY_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# CONTENT CACHE
CONTENT_CACHE_TTL_SECONDS = int(os.getenv("CONTENT_CACHE_TTL_SECONDS", "3600"))
CONTENTFUL_WEBHOOK_SECRET = os.getenv("CONTENTFUL_WEBHOOK_SECRET")
