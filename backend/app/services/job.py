
import logging
from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories import job as job_repository
from app.schemas.job import JobCreate, JobResponse
from app.cache import jobs as job_cache
from app.core.exceptions import JobNotFoundException

logger = logging.getLogger("job-matcher")


def get_jobs(db: Session):
    print("🔥 GET JOBS CALLED")

    cached_jobs = job_cache.get_cached_jobs()

    if cached_jobs is not None:
        logger.info("CACHE HIT: jobs")
        print("CACHE HIT: jobs")
        return cached_jobs

    logger.info("CACHE MISS: jobs")
    print("CACHE MISS: jobs")

    jobs = job_repository.get_all(db)

    jobs_data = [
        JobResponse.model_validate(
            job,
            from_attributes=True
        ).model_dump()
        for job in jobs
    ]

    job_cache.set_cached_jobs(jobs_data)

    return jobs_data


def create_job(db: Session, job_data: JobCreate):
    new_job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        remote=job_data.remote,
        description=job_data.description,
        url=job_data.url
    )

    created_job = job_repository.create(db, new_job)

    job_cache.delete_cached_jobs()

    return created_job


def get_by_id(db: Session, job_id: int):
    found_job = job_repository.get_by_id(db, job_id)

    if found_job is None:
      raise JobNotFoundException()

    return found_job