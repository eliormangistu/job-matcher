from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Job


def get_all(db: Session, limit: int = 20, offset: int = 0):
    return db.scalars(
        select(Job)
        .order_by(Job.id)
        .offset(offset)
        .limit(limit)
    ).all()


def get_all_for_matching(db: Session):
    return db.scalars(select(Job).order_by(Job.id)).all()


def create(db: Session, job: Job):
    db.add(job)
    db.commit()
    db.refresh(job)

    return job

def get_by_id(db: Session, job_id: int):
    return db.get(Job, job_id)

def count_all(db: Session):
    return db.scalar(
        select(func.count()).select_from(Job)
    )
