from fastapi import Header
from google.auth.transport import requests
from google.oauth2 import id_token

from app.core.config import CLIENT_ID, APP_ENV
from app.core.exceptions import AuthenticationException
from app.core.messages import ErrorMessage
from app.core.logger import ServiceLogger


logger = ServiceLogger("auth")


def verify_google_token(
    authorization: str | None = Header(default=None),
):
    logger.info(
        "Google authentication started",
        action="verify_google_token",
    )

    if not authorization:
        logger.warning(
            "Authentication header missing",
            action="verify_google_token",
        )

        print("AUTHORIZATION:", authorization)

        raise AuthenticationException(ErrorMessage.AUTHENTICATION_REQUIRED)

    if not authorization.startswith("Bearer "):
        logger.warning(
            "Invalid authorization format",
            action="verify_google_token",
        )

        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    token = authorization.split(" ", 1)[1]

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            CLIENT_ID,
        )

        logger.info(
            "Google authentication successful",
            action="verify_google_token",
            user_id=idinfo.get("sub"),
        )

    except ValueError:
        logger.warning(
            "Invalid Google token",
            action="verify_google_token",
        )

        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    return idinfo


def verify_user(
    authorization: str | None = Header(default=None),
):
    logger.info(
        "User authentication requested",
        action="verify_user",
        environment=APP_ENV,
    )

    return verify_google_token(authorization)
