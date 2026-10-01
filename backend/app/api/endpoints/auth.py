import re
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.core import StatusCode, SuccessMessage, ErrorMessage
from app.core.security.token.jwt import create_access_token
from app.db.session import get_db
from app.schemas.responses.base import BaseResponse
from app.services.auth import verify_google_token, verify_access_token
from app.services.user import delete_user, get_or_create_user, login_user
from app.schemas.responses.auth import AuthDataResponse
from app.schemas.requests.auth import LoginRequest, RegisterRequest
from app.services.user import register_user
from app.middleware.rate_limit import is_login_allowed
from app.core.security.cookies import (
    delete_access_token_cookie,
    delete_csrf_token_cookie,
    set_access_token_cookie,
    set_csrf_token_cookie,
)
from app.core.security.csrf import generate_csrf_token, require_csrf_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/google_login")
def google_login(
    response: Response,
    idinfo=Depends(verify_google_token),
    db: Session = Depends(get_db),
):
    user = get_or_create_user(
        db=db,
        google_id=idinfo["sub"],
        email=idinfo["email"],
        name=idinfo.get("name", ""),
    )

    access_token = create_access_token(
        user_id=user.id,
    )

    csrf_token = generate_csrf_token()

    set_access_token_cookie(
        response=response,
        access_token=access_token,
    )

    set_csrf_token_cookie(
        response=response,
        csrf_token=csrf_token,
    )

    return BaseResponse[AuthDataResponse](
        True,
        StatusCode.OK,
        SuccessMessage.LOGIN_SUCCESSFUL,
        AuthDataResponse(
            token_type="bearer",
        ),
    )


@router.post("/login")
def login(
    http_request: Request,
    response: Response,
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    if not is_login_allowed(
        request=http_request,
        email=request.email,
        device_id=request.device_id,
    ):
        return BaseResponse(
            False,
            StatusCode.TOO_MANY_REQUESTS,
            ErrorMessage.TOO_MANY_REQUESTS,
            None,
        )

    user = login_user(
        db=db,
        email=request.email,
        password=request.password,
    )

    access_token = create_access_token(user_id=user.id)

    csrf_token = generate_csrf_token()

    set_access_token_cookie(
        response=response,
        access_token=access_token,
    )

    set_csrf_token_cookie(
        response=response,
        csrf_token=csrf_token,
    )

    return BaseResponse[AuthDataResponse](
        True,
        StatusCode.OK,
        SuccessMessage.LOGIN_SUCCESSFUL,
        AuthDataResponse(
            token_type="bearer",
        ),
    )


@router.post("/register")
def register(
    response: Response,
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    user = register_user(
        db=db,
        email=request.email,
        name=request.name,
        password=request.password,
    )

    access_token = create_access_token(
        user_id=user.id,
    )

    csrf_token = generate_csrf_token()

    set_access_token_cookie(
        response=response,
        access_token=access_token,
    )

    set_csrf_token_cookie(
        response=response,
        csrf_token=csrf_token,
    )

    return BaseResponse[AuthDataResponse](
        True,
        StatusCode.OK,
        SuccessMessage.REGISTRATION_SUCCESSFUL,
        AuthDataResponse(
            token_type="bearer",
        ),
    )


@router.post("/logout")
def logout(
    response: Response,
    user=Depends(verify_access_token),
):
    delete_access_token_cookie(response)
    delete_csrf_token_cookie(response)

    return BaseResponse(
        True,
        StatusCode.OK,
        SuccessMessage.LOGOUT_SUCCESSFUL,
        None,
    )


@router.delete("/delete")
def delete_account(
    response: Response,
    user=Depends(verify_access_token),
    _: None = Depends(require_csrf_token),
    db: Session = Depends(get_db),
):
    delete_user(
        db=db,
        user=user,
    )

    delete_access_token_cookie(response)
    delete_csrf_token_cookie(response)

    return BaseResponse(
        True,
        StatusCode.OK,
        SuccessMessage.ACCOUNT_DELETED,
        None,
    )
