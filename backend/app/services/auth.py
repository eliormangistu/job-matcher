from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from google.auth.transport import requests
from google.oauth2 import id_token

from app.core.config import CLIENT_ID, APP_ENV
from app.core.exceptions import AuthenticationException
from app.core.messages import ErrorMessage
from app.core.logger import ServiceLogger
from app.db.session import get_db
from app.core.security.token.jwt import decode_access_token
from .user import get_or_create_user, get_current_user
from app.core.security.cookies import get_access_token_cookie

logger = ServiceLogger("auth")

security = HTTPBearer()


def verify_google_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    logger.info(
        "Google authentication started",
        action="verify_google_token",
    )

    print("GOOGLE CLIENT ID:", CLIENT_ID)
    print("GOOGLE TOKEN RECEIVED:", bool(token))

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

    except ValueError as exc:
        print(
            "GOOGLE TOKEN ERROR:",
            type(exc).__name__,
            str(exc),
        )

        logger.warning(
            "Invalid Google token",
            action="verify_google_token",
        )

        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    return idinfo


def verify_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    logger.info(
        "User authentication requested",
        action="verify_user",
        environment=APP_ENV,
    )

    idinfo = verify_google_token(credentials)

    user = get_or_create_user(
        db=db,
        google_id=idinfo["sub"],
        email=idinfo["email"],
        name=idinfo.get("name", ""),
    )

    return user


def verify_access_token(
    access_token: str | None = Depends(get_access_token_cookie),
    db: Session = Depends(get_db),
):
    if access_token is None:
        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    user_id = decode_access_token(access_token)

    if user_id is None:
        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    user = get_current_user(db=db, user_id=user_id)

    if user is None:
        raise AuthenticationException(ErrorMessage.INVALID_TOKEN)

    return user
