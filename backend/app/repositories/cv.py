from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cv import CV
from app.core.logger import ServiceLogger


logger = ServiceLogger("cv_repository")


def get_by_id(
    db: Session,
    cv_id: int,
) -> CV | None:
    logger.info(
        "Fetching CV by id",
        action="get_by_id",
        cv_id=cv_id,
    )

    cv = db.get(CV, cv_id)

    logger.info(
        "CV lookup completed",
        action="get_by_id",
        cv_id=cv_id,
        found=cv is not None,
    )

    return cv


def get_by_user_id(
    db: Session,
    user_id: int,
) -> CV | None:
    logger.info(
        "Fetching CV by user id",
        action="get_by_user_id",
        user_id=user_id,
    )

    cv = db.scalar(select(CV).where(CV.user_id == user_id))

    logger.info(
        "CV lookup completed",
        action="get_by_user_id",
        user_id=user_id,
        found=cv is not None,
    )

    return cv


def create(
    db: Session,
    cv: CV,
) -> CV:
    logger.info(
        "Creating CV",
        action="create",
        user_id=cv.user_id,
    )

    db.add(cv)
    db.commit()
    db.refresh(cv)

    logger.info(
        "CV created",
        action="create",
        cv_id=cv.id,
        user_id=cv.user_id,
    )

    return cv


def get_all(
    db: Session,
) -> list[CV]:
    logger.info(
        "Fetching all CVs",
        action="get_all",
    )

    cvs = db.scalars(select(CV)).all()

    logger.info(
        "All CVs fetched",
        action="get_all",
        count=len(cvs),
    )

    return cvs
