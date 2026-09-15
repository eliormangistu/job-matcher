from sqlalchemy.orm import Session

from app.repositories import job as job_repository
from app.schemas import JobResponse
from app.cache import jobs as job_cache
from app.core.exceptions import JobNotFoundException
from app.core.logger import ServiceLogger


logger = ServiceLogger("job_service")


def get_jobs(db: Session, limit: int = 20, offset: int = 0):
    logger.info(
        "Fetching jobs",
        action="get_jobs",
        limit=limit,
        offset=offset,
    )

    cached_jobs = job_cache.get_cached_jobs(limit, offset)

    if cached_jobs is not None:
        logger.info(
            "Jobs cache hit",
            action="get_jobs",
            limit=limit,
            offset=offset,
        )

        total = job_repository.count_all(db)

        return cached_jobs, total

    logger.info(
        "Jobs cache miss",
        action="get_jobs",
        limit=limit,
        offset=offset,
    )

    jobs = job_repository.get_all(
        db,
        limit=limit,
        offset=offset,
    )

    total = job_repository.count_all(db)

    logger.info(
        "Jobs fetched from database",
        action="get_jobs",
        count=len(jobs),
        total=total,
    )

    jobs_data = [
        JobResponse.model_validate(
            job,
            from_attributes=True,
        ).model_dump()
        for job in jobs
    ]

    job_cache.set_cached_jobs(
        jobs_data,
        limit,
        offset,
    )

    logger.info(
        "Jobs cached",
        action="get_jobs",
        count=len(jobs_data),
        limit=limit,
        offset=offset,
    )

    return jobs_data, total


def get_by_id(db: Session, job_id: int):
    logger.info(
        "Fetching job",
        action="get_by_id",
        job_id=job_id,
    )

    found_job = job_repository.get_by_id(
        db,
        job_id,
    )

    if found_job is None:
        logger.warning(
            "Job not found",
            action="get_by_id",
            job_id=job_id,
        )

        raise JobNotFoundException()

    logger.info(
        "Job found",
        action="get_by_id",
        job_id=job_id,
    )

    return JobResponse.model_validate(
        found_job,
        from_attributes=True,
    )
