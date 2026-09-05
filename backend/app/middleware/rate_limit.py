from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.rate_limit.rate_limiter import is_allowed
from app.core.status_codes import StatusCode
from app.core.messages import ErrorMessage

class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        if not is_allowed(client_ip):
            return JSONResponse(
                status_code=StatusCode.TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "status_code": StatusCode.TOO_MANY_REQUESTS,
                    "message": ErrorMessage.TOO_MANY_REQUESTS,
                    "data": None
                }
            )

        response = await call_next(request)

        return response