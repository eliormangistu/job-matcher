from sqlalchemy.orm import Session

from app.models.job import Job
from app.core.logger import logger


def get_existing_jobs(
    db: Session,
    airtable_ids: set[str],
) -> dict[str, Job]:
    logger.info(
        "Fetching existing jobs",
        extra={
            "service": "job_repository_worker",
            "action": "get_existing_jobs",
            "requested_count": len(airtable_ids),
        },
    )

    jobs = {
        job.airtable_id: job
        for job in db.query(Job).filter(Job.airtable_id.in_(airtable_ids)).all()
    }

    logger.info(
        "Existing jobs fetched",
        extra={
            "service": "job_repository_worker",
            "action": "get_existing_jobs",
            "found_count": len(jobs),
        },
    )

    return jobs


def create_job(db: Session, job_data: dict) -> Job:
    job = Job(
        airtable_id=job_data["airtable_id"],
        job_id=job_data.get("job_id"),
        title=job_data.get("title"),
        company=job_data.get("company"),
        location=job_data.get("location"),
        remote=False,
        description=job_data.get("job_description"),
        url=job_data.get("position_link"),
        field=job_data.get("field"),
        company_industry=job_data.get("company_industry"),
        min_experience=job_data.get("min_experience"),
        requirements=job_data.get("requirements"),
        required_skills=[],
        language_requirement=job_data.get("language_requirement"),
        education_requirements=job_data.get("education_requirements"),
        posted=job_data.get("posted"),
    )

    db.add(job)

    logger.info(
        "Job created in session",
        extra={
            "service": "job_repository_worker",
            "action": "create_job",
            "airtable_id": job_data["airtable_id"],
            "job_id": job_data.get("job_id"),
        },
    )

    return job


def update_job(job: Job, job_data: dict) -> bool:
    changed = False

    fields = {
        "job_id": job_data.get("job_id"),
        "title": job_data.get("title"),
        "company": job_data.get("company"),
        "location": job_data.get("location"),
        "description": job_data.get("job_description"),
        "url": job_data.get("position_link"),
        "field": job_data.get("field"),
        "company_industry": job_data.get("company_industry"),
        "min_experience": job_data.get("min_experience"),
        "requirements": job_data.get("requirements"),
        "language_requirement": job_data.get("language_requirement"),
        "education_requirements": job_data.get("education_requirements"),
        "posted": job_data.get("posted"),
    }

    changed_fields = []

    for field, new_value in fields.items():
        if getattr(job, field) != new_value:
            setattr(job, field, new_value)
            changed = True
            changed_fields.append(field)

    if changed:
        logger.info(
            "Job updated",
            extra={
                "service": "job_repository_worker",
                "action": "update_job",
                "airtable_id": job.airtable_id,
                "job_id": job.id,
                "changed_fields": changed_fields,
            },
        )

    return changed
