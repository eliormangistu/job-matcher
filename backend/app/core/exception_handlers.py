from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    InvalidCSRFTokenException,
    InvalidFileException,
    JobNotFoundException,
    AuthenticationException,
    UserAlreadyExistsException,
    GeminiException,
)
from app.core import ErrorMessage, StatusCode
from app.schemas import BaseResponse


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


async def gemini_exception_handler(
    request: Request,
    exc: GeminiException,
):
    response = BaseResponse(
        False,
        exc.status_code,
        ErrorMessage.AI_SERVICE_UNAVAILABLE,
        None,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsException,
):
    response = BaseResponse(
        False,
        StatusCode.CONFLICT,
        str(exc),
        None,
    )

    return JSONResponse(
        status_code=StatusCode.CONFLICT,
        content=response.model_dump(),
    )


def invalid_csrf_token_handler(
    request,
    exc: InvalidCSRFTokenException,
):
    return JSONResponse(
        status_code=StatusCode.FORBIDDEN,
        content=BaseResponse(
            False,
            StatusCode.FORBIDDEN,
            ErrorMessage.INVALID_CSRF_TOKEN,
            None,
        ).model_dump(),
    )


def invalid_file_handler(
    request,
    exc: InvalidFileException,
):
    return JSONResponse(
        status_code=StatusCode.BAD_REQUEST,
        content=BaseResponse(
            False,
            StatusCode.BAD_REQUEST,
            ErrorMessage.INVALID_FILE,
            None,
        ).model_dump(),
    )
