from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.rate_limit import is_allowed
from app.core.status_codes import StatusCode
from app.core.messages import ErrorMessage
from app.core.logger import ServiceLogger


logger = ServiceLogger("rate_limit_middleware")


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "Rate limit check started",
            action="dispatch",
            method=request.method,
            path=request.url.path,
        )

        if not is_allowed(client_ip):
            logger.warning(
                "Request blocked by rate limit",
                action="dispatch",
                method=request.method,
                path=request.url.path,
                status_code=StatusCode.TOO_MANY_REQUESTS,
            )

            return JSONResponse(
                status_code=StatusCode.TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "status_code": StatusCode.TOO_MANY_REQUESTS,
                    "message": ErrorMessage.TOO_MANY_REQUESTS,
                    "data": None,
                },
            )

        response = await call_next(request)

        logger.info(
            "Request passed rate limit",
            action="dispatch",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )

        return response
