from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    JWT_ISSUER,
)
from app.core.logger import ServiceLogger


logger = ServiceLogger("jwt")


def create_access_token(
    user_id: int,
) -> str:
    logger.info(
        "Creating access token",
        action="create_access_token",
        user_id=user_id,
    )

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(
        minutes=JWT_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "iat": issued_at,
        "exp": expires_at,
        "iss": JWT_ISSUER,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    logger.info(
        "Access token created successfully",
        action="create_access_token",
        user_id=user_id,
    )

    return token


def decode_access_token(token: str) -> int | None:
    logger.info(
        "Decoding access token",
        action="decode_access_token",
    )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
        )

        user_id = payload.get("sub")

        if user_id is None:
            logger.warning(
                "Access token missing user id",
                action="decode_access_token",
            )
            return None

        user_id = int(user_id)

        logger.info(
            "Access token decoded successfully",
            action="decode_access_token",
            user_id=user_id,
        )

        return user_id

    except (jwt.InvalidTokenError, ValueError):
        logger.warning(
            "Invalid access token",
            action="decode_access_token",
        )
        return None
