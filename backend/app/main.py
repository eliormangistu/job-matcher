import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.router import api_router
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.core.exceptions import (
    JobNotFoundException,
    AuthenticationException,
)

from app.core.exception_handlers import (
    job_not_found_handler,
    validation_exception_handler,
    authentication_exception_handler,
)
from app.middleware.rate_limit import RateLimitMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

app = FastAPI(title="Job Matcher")

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    JobNotFoundException,
    job_not_found_handler
)

app.add_exception_handler(
    AuthenticationException,
    authentication_exception_handler
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

app.include_router(api_router)