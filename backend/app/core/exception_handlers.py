from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    JobNotFoundException,
    AuthenticationException,
)
from app.core import ErrorMessage, StatusCode
from app.schemas.common import BaseResponse


async def job_not_found_handler(request: Request, exc: JobNotFoundException):
    response = BaseResponse(
        False, StatusCode.NOT_FOUND, ErrorMessage.JOB_NOT_FOUND, None
    )

    return JSONResponse(status_code=StatusCode.NOT_FOUND, content=response.model_dump())


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response = BaseResponse(
        False, StatusCode.UNPROCESSABLE_ENTITY, ErrorMessage.INVALID_REQUEST, None
    )

    return JSONResponse(
        status_code=StatusCode.UNPROCESSABLE_ENTITY, content=response.model_dump()
    )


async def authentication_exception_handler(
    request: Request, exc: AuthenticationException
):
    response = BaseResponse(False, StatusCode.UNAUTHORIZED, str(exc), None)

    return JSONResponse(
        status_code=StatusCode.UNAUTHORIZED, content=response.model_dump()
    )
