import json
from datetime import datetime

from app.core.logger import ServiceLogger
from app.db.session import SessionLocal
from app.models.job import Job


logger = ServiceLogger("job_import")

INPUT_FILE = "data/jobs.json"


def import_jobs():
    logger.info(
        "Job import started",
        action="import_jobs",
        input_file=INPUT_FILE,
    )

    with open(INPUT_FILE, encoding="utf-8") as f:
        jobs_data = json.load(f)

    logger.info(
        "Jobs file loaded",
        action="load_jobs",
        count=len(jobs_data),
    )

    db = SessionLocal()

    created_count = 0
    updated_count = 0
    deleted_count = 0

    try:
        for job_data in jobs_data:
            airtable_id = job_data.get("airtable_id") or job_data.get("id")

            if not airtable_id:
                logger.error(
                    "Job is missing Airtable record ID",
                    action="validate_job",
                )
                raise ValueError("Each imported job must include an Airtable record ID")

            posted = (
                datetime.fromisoformat(job_data["posted"].replace("Z", "+00:00"))
                .date()
                .isoformat()
                if job_data.get("posted")
                else None
            )

            job = db.query(Job).filter(Job.airtable_id == airtable_id).first()

            if job:
                job.job_id = job_data.get("job_id")
                job.title = job_data.get("title")
                job.company = job_data.get("company")
                job.location = job_data.get("location")
                job.remote = False
                job.description = job_data.get("job_description")
                job.url = job_data.get("position_link")
                job.field = job_data.get("field")
                job.company_industry = job_data.get("company_industry")
                job.min_experience = job_data.get("min_experience")
                job.requirements = job_data.get("requirements")
                job.language_requirement = job_data.get("language_requirement")
                job.education_requirements = job_data.get("education_requirements")
                job.posted = posted

                updated_count += 1

            else:
                job = Job(
                    airtable_id=airtable_id,
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
                    language_requirement=job_data.get("language_requirement"),
                    education_requirements=job_data.get("education_requirements"),
                    posted=posted,
                )

                db.add(job)
                created_count += 1

        imported_airtable_ids = {
            job_data.get("airtable_id") or job_data.get("id") for job_data in jobs_data
        }

        jobs_to_delete = (
            db.query(Job).filter(~Job.airtable_id.in_(imported_airtable_ids)).all()
        )

        deleted_count = len(jobs_to_delete)

        for job in jobs_to_delete:
            db.delete(job)

        db.commit()

        logger.info(
            "Job import completed",
            action="import_jobs",
            created_count=created_count,
            updated_count=updated_count,
            deleted_count=deleted_count,
            total_jobs=len(jobs_data),
        )

        print(f"Created: {created_count}")
        print(f"Updated: {updated_count}")
        print(f"Deleted: {deleted_count}")
        print(f"Imported {created_count + updated_count} jobs successfully.")

    except Exception:
        db.rollback()

        logger.exception(
            "Job import failed",
            action="import_jobs",
        )

        raise

    finally:
        db.close()

        logger.info(
            "Job import database session closed",
            action="cleanup",
        )


if __name__ == "__main__":
    import_jobs()
