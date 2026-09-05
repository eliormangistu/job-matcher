import json

from app.db.session import SessionLocal
from app.models.job import Job
from datetime import datetime

INPUT_FILE = "jobs.json"


with open(INPUT_FILE, encoding="utf-8") as f:
    jobs_data = json.load(f)


db = SessionLocal()

try:
    jobs = []

    for job_data in jobs_data:
        airtable_id = job_data.get("airtable_id") or job_data.get("id")
        if not airtable_id:
            raise ValueError("Each imported job must include an Airtable record ID")

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
            salary=job_data.get("salary"),
            point_of_contact=job_data.get("point_of_contact"),
            linkedin=job_data.get("linkedin"),
            email=job_data.get("email"),
            phone=job_data.get("phone"),
            posted=(
                datetime.fromisoformat(job_data["posted"].replace("Z", "+00:00"))
                .date()
                .isoformat()
                if job_data.get("posted")
                else None
            ),
        )

        jobs.append(job)

    db.add_all(jobs)
    db.commit()

    print(f"Imported {len(jobs)} jobs successfully.")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
