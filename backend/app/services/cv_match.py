from sqlalchemy.orm import Session

from app.models.cv_match import CVMatch
from app.repositories.cv_match import delete_by_cv_id, create_many, get_by_cv_id
from app.repositories.cv import get_by_id, get_all
from app.repositories.job import get_all_for_matching
from app.services.matching.matcher import rank_jobs
from app.services.cv import build_candidate_profile
from app.schemas.match import JobMatch
from app.schemas.responses.job import JobResponse
from app.core.logger import ServiceLogger


logger = ServiceLogger("cv_match")


def save_matches(
    db: Session,
    cv_id: int,
    matches: list[JobMatch],
) -> list[CVMatch]:
    logger.info(
        "Saving CV matches",
        action="save_matches",
        cv_id=cv_id,
        count=len(matches),
    )

    delete_by_cv_id(
        db=db,
        cv_id=cv_id,
    )

    cv_matches = [
        CVMatch(
            cv_id=cv_id,
            job_id=match.job_id,
            score=match.score,
            matched_skills=match.matched_skills,
            missing_skills=match.missing_skills,
        )
        for match in matches
    ]

    if not cv_matches:
        logger.info(
            "No CV matches to save",
            action="save_matches",
            cv_id=cv_id,
        )
        return []

    saved_matches = create_many(
        db=db,
        matches=cv_matches,
    )

    logger.info(
        "CV matches saved successfully",
        action="save_matches",
        cv_id=cv_id,
        count=len(saved_matches),
    )

    return saved_matches


def refresh_matches_for_cv(db: Session, cv_id: int) -> list[CVMatch]:
    print("REFRESH 1 - getting CV")

    cv = get_by_id(db=db, cv_id=cv_id)

    print("REFRESH 2 - CV:", cv)

    if cv is None:
        return []

    print("REFRESH 3 - building candidate")

    candidate = build_candidate_profile(cv)

    print("REFRESH 4 - candidate:", candidate)

    print("REFRESH 5 - getting jobs")

    jobs = get_all_for_matching(db)

    print("REFRESH 6 - jobs:", len(jobs))

    print("REFRESH 7 - ranking")

    try:
        matches = rank_jobs(candidate, jobs)
    except Exception as e:
        print("REFRESH ERROR - ranking:", repr(e))
        print("REFRESH ERROR TYPE:", type(e))
        raise

    print("REFRESH 8 - matches:", len(matches))

    print("REFRESH 9 - saving")

    saved_matches = save_matches(
        db=db,
        cv_id=cv.id,
        matches=matches,
    )

    print("REFRESH 10 - saved:", len(saved_matches))

    return saved_matches


def get_job_matches_for_cv(
    db: Session,
    cv_id: int,
) -> list[JobMatch]:
    logger.info(
        "Fetching job matches for CV",
        action="get_job_matches_for_cv",
        cv_id=cv_id,
    )

    matches = get_by_cv_id(
        db=db,
        cv_id=cv_id,
    )

    job_matches = [
        JobMatch(
            job_id=match.job_id,
            score=match.score,
            matched_skills=match.matched_skills,
            missing_skills=match.missing_skills,
            job=JobResponse.model_validate(
                match.job,
                from_attributes=True,
            ),
        )
        for match in matches
    ]

    logger.info(
        "Job matches fetched successfully",
        action="get_job_matches_for_cv",
        cv_id=cv_id,
        count=len(job_matches),
    )

    return job_matches


def refresh_all_cv_matches(
    db: Session,
) -> None:
    logger.info(
        "Refreshing matches for all CVs",
        action="refresh_all_cv_matches",
    )

    cvs = get_all(
        db=db,
    )

    for cv in cvs:
        refresh_matches_for_cv(
            db=db,
            cv_id=cv.id,
        )

    logger.info(
        "All CV matches refreshed successfully",
        action="refresh_all_cv_matches",
        count=len(cvs),
    )
