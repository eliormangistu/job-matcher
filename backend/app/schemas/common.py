from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    status_code: int
    message: str
    data: T | None

    def __init__(
        self,
        success: bool,
        status_code: int,
        message: str,
        data: T | None
    ):
        super().__init__(
            success=success,
            status_code=status_code,
            message=message,
            data=data
        )