from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Job
from app.core.logger import logger


def get_all(db: Session, limit: int = 20, offset: int = 0):
    logger.info(
        "Fetching jobs",
        extra={
            "service": "job_repository",
            "action": "get_all",
            "limit": limit,
            "offset": offset,
        },
    )

    jobs = db.scalars(select(Job).order_by(Job.id).offset(offset).limit(limit)).all()

    logger.info(
        "Jobs fetched",
        extra={
            "service": "job_repository",
            "action": "get_all",
            "count": len(jobs),
            "limit": limit,
            "offset": offset,
        },
    )

    return jobs


def get_all_for_matching(db: Session):
    logger.info(
        "Fetching jobs for matching",
        extra={
            "service": "job_repository",
            "action": "get_all_for_matching",
        },
    )

    jobs = db.scalars(select(Job).order_by(Job.id)).all()

    logger.info(
        "Jobs fetched for matching",
        extra={
            "service": "job_repository",
            "action": "get_all_for_matching",
            "count": len(jobs),
        },
    )

    return jobs


def create(db: Session, job: Job):
    logger.info(
        "Creating job",
        extra={
            "service": "job_repository",
            "action": "create",
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    logger.info(
        "Job created",
        extra={
            "service": "job_repository",
            "action": "create",
            "job_id": job.id,
        },
    )

    return job


def get_by_id(db: Session, job_id: int):
    logger.info(
        "Fetching job by id",
        extra={
            "service": "job_repository",
            "action": "get_by_id",
            "job_id": job_id,
        },
    )

    job = db.get(Job, job_id)

    logger.info(
        "Job lookup completed",
        extra={
            "service": "job_repository",
            "action": "get_by_id",
            "job_id": job_id,
            "found": job is not None,
        },
    )

    return job


def count_all(db: Session):
    logger.info(
        "Counting jobs",
        extra={
            "service": "job_repository",
            "action": "count_all",
        },
    )

    total = db.scalar(select(func.count()).select_from(Job)) or 0

    logger.info(
        "Jobs counted",
        extra={
            "service": "job_repository",
            "action": "count_all",
            "total": total,
        },
    )

    return total
