from app.db.session import SessionLocal
from app.models.job import Job


db = SessionLocal()

job = Job(
    airtable_id="seed-full-stack-developer",
    title="Full Stack Developer",
    company="Tech Company",
    location="Tel Aviv",
    remote=True,
    description="We are looking for a Full Stack Developer with experience in React, Python and PostgreSQL.",
    url="https://example.com/jobs/full-stack-developer"
)

db.add(job)
db.commit()
db.refresh(job)

print(f"Job created with ID: {job.id}")

db.close()
