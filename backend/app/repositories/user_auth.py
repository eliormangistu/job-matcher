from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import ServiceLogger
from app.models.user_auth import UserAuth


logger = ServiceLogger("user_auth_repository")


def get_by_user_id(
    db: Session,
    user_id: int,
) -> UserAuth | None:
    logger.info(
        "Fetching user auth by user id",
        action="get_by_user_id",
        user_id=user_id,
    )

    user_auth = db.scalar(select(UserAuth).where(UserAuth.user_id == user_id))

    logger.info(
        "User auth lookup completed",
        action="get_by_user_id",
        user_id=user_id,
        found=user_auth is not None,
    )

    return user_auth


def create(
    db: Session,
    user_auth: UserAuth,
) -> UserAuth:
    logger.info(
        "Creating user auth",
        action="create",
        user_id=user_auth.user_id,
    )

    db.add(user_auth)
    db.commit()
    db.refresh(user_auth)

    logger.info(
        "User auth created",
        action="create",
        user_id=user_auth.user_id,
    )

    return user_auth


def add(
    db: Session,
    user_auth: UserAuth,
) -> UserAuth:
    logger.info(
        "Adding user auth",
        action="add",
        user_id=user_auth.user_id,
    )

    db.add(user_auth)
    db.flush()

    logger.info(
        "User auth added",
        action="add",
        user_id=user_auth.user_id,
    )

    return user_auth
