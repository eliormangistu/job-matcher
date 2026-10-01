import os

# DATABASE

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = os.getenv("DATABASE_URL")

# REDIS

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

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
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

# AIRTABLE
AIRTABLE_VIEW_URL = (
    "https://airtable.com/embed/"
    "appwewqLk7iUY4azc/"
    "shrQBuWjXd0YgPqV6"
    "?backgroundColor=cyan&viewControls=on"
)

# CONTENT
SPACE_ID = os.getenv("SPACE_ID", "")
ENTRY_ID = os.getenv("ENTRY_ID", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")

# CONTENT CACHE
CONTENT_CACHE_TTL_SECONDS = int(os.getenv("CONTENT_CACHE_TTL_SECONDS", "3600"))
CONTENTFUL_WEBHOOK_SECRET = os.getenv("CONTENTFUL_WEBHOOK_SECRET", "")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
JWT_ISSUER = os.getenv(
    "JWT_ISSUER",
    "job-matcher",
)

# COOCKIES
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")
COOKIE_MAX_AGE = int(
    os.getenv(
        "COOKIE_MAX_AGE",
        "3600",
    )
)

# FILE
MAX_CV_FILE_SIZE = int(os.getenv("MAX_CV_FILE_SIZE", str(5 * 1024 * 1024)))

ALLOWED_CV_EXTENSIONS = {
    extension.strip().lower()
    for extension in os.getenv(
        "ALLOWED_CV_EXTENSIONS",
        ".pdf",
    ).split(",")
    if extension.strip()
}

ALLOWED_CV_CONTENT_TYPES = {
    content_type.strip().lower()
    for content_type in os.getenv(
        "ALLOWED_CV_CONTENT_TYPES",
        "application/pdf",
    ).split(",")
    if content_type.strip()
}


# HTTPS
HSTS_ENABLED = (
    os.getenv(
        "HSTS_ENABLED",
        "false",
    ).lower()
    == "true"
)

HSTS_MAX_AGE = int(
    os.getenv(
        "HSTS_MAX_AGE",
        "31536000",
    )
)
