
import logging
from sqlalchemy.orm import Session

from app.models import Job
from app.repositories import job as job_repository
from app.schemas import JobResponse
from app.cache import jobs as job_cache
from app.core.exceptions import JobNotFoundException

logger = logging.getLogger("job-matcher")



def get_jobs(db: Session, limit: int = 20, offset: int = 0):

    cached_jobs = job_cache.get_cached_jobs(limit, offset)

    if cached_jobs is not None:
        logger.info("CACHE HIT: jobs")
        return cached_jobs

    logger.info("CACHE MISS: jobs")

    jobs = job_repository.get_all(
        db,
        limit=limit,
        offset=offset
    )

    jobs_data = [
        JobResponse.model_validate(
            job,
            from_attributes=True
        ).model_dump()
        for job in jobs
    ]

    job_cache.set_cached_jobs(
        jobs_data,
        limit,
        offset
    )

    return jobs_data


def get_by_id(db: Session, job_id: int):
    found_job = job_repository.get_by_id(db, job_id)

    if found_job is None:
      raise JobNotFoundException()

    found_job = JobResponse.model_validate(
        found_job,
        from_attributes=True
    )

    return found_job