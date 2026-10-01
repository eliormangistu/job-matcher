from fastapi import Cookie, Response
from app.core.config import COOKIE_SECURE, COOKIE_SAMESITE, COOKIE_MAX_AGE

ACCESS_TOKEN_COOKIE = "access_token"
CSRF_TOKEN_COOKIE = "csrf_token"


def set_access_token_cookie(
    response: Response,
    access_token: str,
) -> None:
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=COOKIE_MAX_AGE,
        path="/",
    )


def get_access_token_cookie(
    access_token: str | None = Cookie(default=None),
) -> str | None:
    return access_token


def delete_access_token_cookie(
    response: Response,
) -> None:
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE,
        path="/",
    )


def set_csrf_token_cookie(
    response: Response,
    csrf_token: str,
) -> None:
    response.set_cookie(
        key=CSRF_TOKEN_COOKIE,
        value=csrf_token,
        httponly=False,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=COOKIE_MAX_AGE,
        path="/",
    )


def delete_csrf_token_cookie(
    response: Response,
) -> None:
    response.delete_cookie(
        key=CSRF_TOKEN_COOKIE,
        path="/",
    )
