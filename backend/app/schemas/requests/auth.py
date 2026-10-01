from pydantic import EmailStr, Field
from .base import BaseRequest


class RegisterRequest(BaseRequest):
    email: EmailStr
    name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)


class LoginRequest(BaseRequest):
    email: EmailStr
    password: str = Field(min_length=8)
    device_id: str = Field(min_length=16, max_length=255)
