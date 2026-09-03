from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    status_code: int
    message: str
    data: T | None