import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        request_id = getattr(
            request.state,
            "request_id",
            "N/A",
        )

        logger.info(
            "Request completed",
            extra={
                "service": "request_logging",
                "action": "request",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "request_id": request_id,
            },
        )

        return response
