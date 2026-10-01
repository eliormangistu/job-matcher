from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.router import api_router
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.core.exceptions import (
    InvalidCSRFTokenException,
    InvalidFileException,
    JobNotFoundException,
    AuthenticationException,
    GeminiException,
    UserAlreadyExistsException,
)

from app.core.exception_handlers import (
    invalid_csrf_token_handler,
    invalid_file_handler,
    job_not_found_handler,
    validation_exception_handler,
    authentication_exception_handler,
    gemini_exception_handler,
    user_already_exists_handler,
)
from app.middleware.rate_limit import RateLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.core.logger import configure_logging
from app.core.security.headers import SecurityHeadersMiddleware

configure_logging()

app = FastAPI(title="Job Matcher")

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("CORS_ORIGINS:", CORS_ORIGINS)

app.add_exception_handler(
    InvalidCSRFTokenException,
    invalid_csrf_token_handler,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_exception_handler(JobNotFoundException, job_not_found_handler)

app.add_exception_handler(AuthenticationException, authentication_exception_handler)

app.add_exception_handler(UserAlreadyExistsException, user_already_exists_handler)

app.add_exception_handler(InvalidFileException, invalid_file_handler)

app.add_exception_handler(GeminiException, gemini_exception_handler)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

app.include_router(api_router)
