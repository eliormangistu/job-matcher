from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import JobNotFoundException
from app.core.messages import ErrorMessage
from app.core.status_codes import StatusCode


async def job_not_found_handler(
    request: Request,
    exc: JobNotFoundException
):
    return JSONResponse(
        status_code=StatusCode.NOT_FOUND,
        content={
            "success": False,
            "status_code": StatusCode.NOT_FOUND,
            "message": ErrorMessage.JOB_NOT_FOUND,
            "data": None
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=StatusCode.UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "status_code": StatusCode.UNPROCESSABLE_ENTITY,
            "message": ErrorMessage.INVALID_REQUEST,
            "data": None
        }
    )