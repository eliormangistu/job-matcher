from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    google_id: str | None
    email: str
    name: str
    created_at: datetime
    updated_at: datetime


class UserData(BaseModel):
    user: UserResponse
