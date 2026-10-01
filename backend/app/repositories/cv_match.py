from app.models.cv import CV
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.cv_match import CVMatch
from app.core.logger import ServiceLogger


logger = ServiceLogger("cv_match_repository")


def get_by_cv_id(
    db: Session,
    cv_id: int,
) -> list[CVMatch]:
    logger.info(
        "Fetching CV matches",
        action="get_by_cv_id",
        cv_id=cv_id,
    )

    matches = db.scalars(
        select(CVMatch).where(CVMatch.cv_id == cv_id).order_by(CVMatch.score.desc())
    ).all()

    logger.info(
        "CV matches fetched",
        action="get_by_cv_id",
        cv_id=cv_id,
        count=len(matches),
    )

    return matches


def delete_by_cv_id(
    db: Session,
    cv_id: int,
) -> None:
    logger.info(
        "Deleting CV matches",
        action="delete_by_cv_id",
        cv_id=cv_id,
    )

    db.execute(delete(CVMatch).where(CVMatch.cv_id == cv_id))
    db.commit()

    logger.info(
        "CV matches deleted",
        action="delete_by_cv_id",
        cv_id=cv_id,
    )


def create_many(
    db: Session,
    matches: list[CVMatch],
) -> list[CVMatch]:
    logger.info(
        "Creating CV matches",
        action="create_many",
        count=len(matches),
    )

    db.add_all(matches)
    db.commit()

    for match in matches:
        db.refresh(match)

    logger.info(
        "CV matches created",
        action="create_many",
        count=len(matches),
    )

    return matches


def get_latest_by_user_id(
    db: Session,
    user_id: int,
) -> CV | None:
    logger.info(
        "Fetching latest CV by user id",
        action="get_latest_by_user_id",
        user_id=user_id,
    )

    cv = db.scalar(
        select(CV).where(CV.user_id == user_id).order_by(CV.created_at.desc()).limit(1)
    )

    logger.info(
        "Latest CV lookup completed",
        action="get_latest_by_user_id",
        user_id=user_id,
        found=cv is not None,
    )

    return cv


def update(
    db: Session,
    cv: CV,
) -> CV:
    logger.info(
        "Updating CV",
        action="update",
        cv_id=cv.id,
        user_id=cv.user_id,
    )

    db.commit()
    db.refresh(cv)

    logger.info(
        "CV updated",
        action="update",
        cv_id=cv.id,
        user_id=cv.user_id,
    )

    return cv
