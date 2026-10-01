from pydantic import BaseModel


class AuthDataResponse(BaseModel):
    token_type: str
