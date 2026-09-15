import json

from datetime import datetime

from app.db.session import SessionLocal
from app.core.logger import ServiceLogger

from app.workers.job_repository import (
    create_job,
    get_existing_jobs,
    update_job,
)


logger = ServiceLogger("job_sync")

INPUT_FILE = "data/jobs.json"


def sync_jobs():
    logger.info(
        "Job sync started",
        action="sync_jobs",
        input_file=INPUT_FILE,
    )

    with open(INPUT_FILE, encoding="utf-8") as f:
        jobs_data = json.load(f)

    logger.info(
        "Jobs file loaded",
        action="load_jobs",
        count=len(jobs_data),
    )

    airtable_ids = {
        job_data.get("airtable_id") or job_data.get("id") for job_data in jobs_data
    }

    db = SessionLocal()

    try:
        existing_jobs = get_existing_jobs(
            db,
            airtable_ids,
        )

        logger.info(
            "Existing jobs loaded",
            action="get_existing_jobs",
            count=len(existing_jobs),
        )

        new_jobs = 0
        updated_jobs = 0

        for job_data in jobs_data:
            airtable_id = job_data.get("airtable_id") or job_data.get("id")

            if not airtable_id:
                logger.error(
                    "Job is missing Airtable record ID",
                    action="validate_job",
                )

                raise ValueError("Each imported job must include an Airtable record ID")

            job_data["airtable_id"] = airtable_id

            job_data["posted"] = (
                datetime.fromisoformat(job_data["posted"].replace("Z", "+00:00"))
                .date()
                .isoformat()
                if job_data.get("posted")
                else None
            )

            existing_job = existing_jobs.get(airtable_id)

            if existing_job:
                changed = update_job(
                    existing_job,
                    job_data,
                )

                if changed:
                    updated_jobs += 1

            else:
                create_job(
                    db,
                    job_data,
                )
                new_jobs += 1

        db.commit()

        logger.info(
            "Job sync completed",
            action="sync_jobs",
            new_jobs=new_jobs,
            updated_jobs=updated_jobs,
            total_jobs=len(jobs_data),
        )

    except Exception:
        db.rollback()

        logger.exception(
            "Job sync failed",
            action="sync_jobs",
        )

        raise

    finally:
        db.close()

        logger.info(
            "Job sync database session closed",
            action="cleanup",
        )


if __name__ == "__main__":
    sync_jobs()
