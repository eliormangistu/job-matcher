from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services import job
from app.schemas.common import BaseResponse
from app.core.messages import SuccessMessage
from app.core.status_codes import StatusCode

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("", response_model=BaseResponse[list[JobResponse]])
def get_jobs(db: Session = Depends(get_db)):
    jobs = job.get_jobs(db)
    return BaseResponse(
        success=True,
        status_code=StatusCode.OK,
        message=SuccessMessage.JOBS_RETRIEVED,
        data=jobs
    )


@router.post("", response_model=BaseResponse[JobResponse],
    status_code=StatusCode.CREATED)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    created_job = job.create_job(db, job_data)
    return BaseResponse(
        success=True,
        status_code=StatusCode.CREATED,
        message=SuccessMessage.JOB_CREATED,
        data=created_job
    )

@router.get("/{job_id}", response_model=BaseResponse[JobResponse])
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    found_job = job.get_by_id(db, job_id)
    return BaseResponse(
        success=True,
        status_code=StatusCode.OK,
        message=SuccessMessage.JOB_RETRIEVED,
        data=found_job
    )