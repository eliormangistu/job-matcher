import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("job-matcher")


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        request_id = getattr(
            request.state,
            "request_id",
            "N/A"
        )

        logger.info(
            "%s %s | %s | %.2fms | request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration * 1000,
            request_id
        )

        return response