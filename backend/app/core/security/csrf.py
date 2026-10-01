import secrets
from fastapi import Header, Request
from app.core.exceptions import InvalidCSRFTokenException

CSRF_TOKEN_LENGTH = 32
CSRF_HEADER_NAME = "X-CSRF-Token"
CSRF_COOCKIE_NAME = "csrf_token"


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(CSRF_TOKEN_LENGTH)


def validate_csrf_token(
    request: Request,
    csrf_header: str | None,
) -> bool:
    csrf_cookie = request.cookies.get(CSRF_COOCKIE_NAME)

    if not csrf_cookie or not csrf_header:
        return False

    return secrets.compare_digest(
        csrf_cookie,
        csrf_header,
    )


def require_csrf_token(
    request: Request,
    csrf_header: str | None = Header(
        default=None,
        alias=CSRF_HEADER_NAME,
    ),
) -> None:
    if not validate_csrf_token(
        request=request,
        csrf_header=csrf_header,
    ):
        raise InvalidCSRFTokenException()
