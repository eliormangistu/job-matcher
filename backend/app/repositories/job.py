from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job


def get_all(db: Session):
    return db.scalars(select(Job)).all()


def create(db: Session, job: Job):
    db.add(job)
    db.commit()
    db.refresh(job)

    return job

def get_by_id(db: Session, job_id: int):
    return db.get(Job, job_id)