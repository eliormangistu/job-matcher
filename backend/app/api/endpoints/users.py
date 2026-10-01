from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.auth import verify_access_token
from app.db.session import get_db
from app.schemas.responses.base import BaseResponse
from app.services.user import get_current_user
from app.core import StatusCode, SuccessMessage
from app.schemas.responses.user import UserData, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/get_user",
    response_model=BaseResponse[UserData],
)
def get_user(
    user=Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    current_user = get_current_user(
        db=db,
        user_id=user.id,
    )

    if current_user is None:
        return BaseResponse[UserData](
            False,
            StatusCode.NOT_FOUND,
            "User not found",
            None,
        )

    return BaseResponse[UserData](
        True,
        StatusCode.OK,
        SuccessMessage.USER_FETCHED,
        UserData(
            user=UserResponse.model_validate(
                current_user,
                from_attributes=True,
            )
        ),
    )
