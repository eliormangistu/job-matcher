from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Job
from app.core.logger import ServiceLogger


logger = ServiceLogger("job_repository")


def get_all(db: Session, limit: int = 20, offset: int = 0):
    logger.info(
        "Fetching jobs",
        action="get_all",
        limit=limit,
        offset=offset,
    )

    jobs = db.scalars(
        select(Job)
        .order_by(
            Job.posted.desc(),
            Job.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    ).all()

    logger.info(
        "Jobs fetched",
        action="get_all",
        count=len(jobs),
        limit=limit,
        offset=offset,
    )

    return jobs


def get_all_for_matching(db: Session):
    logger.info(
        "Fetching jobs for matching",
        action="get_all_for_matching",
    )

    jobs = db.scalars(select(Job).order_by(Job.id)).all()

    logger.info(
        "Jobs fetched for matching",
        action="get_all_for_matching",
        count=len(jobs),
    )

    return jobs


def create(db: Session, job: Job):
    logger.info(
        "Creating job",
        action="create",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    logger.info(
        "Job created",
        action="create",
        job_id=job.id,
    )

    return job


def get_by_id(db: Session, job_id: int):
    logger.info(
        "Fetching job by id",
        action="get_by_id",
        job_id=job_id,
    )

    job = db.get(Job, job_id)

    logger.info(
        "Job lookup completed",
        action="get_by_id",
        job_id=job_id,
        found=job is not None,
    )

    return job


def count_all(db: Session):
    logger.info(
        "Counting jobs",
        action="count_all",
    )

    total = db.scalar(select(func.count()).select_from(Job)) or 0

    logger.info(
        "Jobs counted",
        action="count_all",
        total=total,
    )

    return total
