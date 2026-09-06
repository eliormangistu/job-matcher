from fastapi import Header
from google.auth.transport import requests
from google.oauth2 import id_token

from app.core.config import CLIENT_ID, APP_ENV
from app.core.exceptions import AuthenticationException
from app.core.messages import ErrorMessage


def verify_google_token(authorization: str | None = Header(default=None)):
    if not authorization:
        raise AuthenticationException(ErrorMessage.AUTHENTICATION_REQUIRED)

    if not authorization.startswith("Bearer "):
        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    token = authorization.split(" ", 1)[1]

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except ValueError:
        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    return idinfo


def _verify_dev_user():
    return {
        "sub": "dev-user",
        "email": "dev@example.com",
    }


def verify_user(authorization: str | None = Header(default=None)):
    if APP_ENV != "prod":
        return _verify_dev_user()

    return verify_google_token(authorization)
