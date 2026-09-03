from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import JobCreate, JobResponse
from app.services import (
    create_job as create_job_service,
    get_jobs as get_jobs_service,
    get_by_id as get_by_id_service,
)
from app.schemas import BaseResponse
from app.core.messages import SuccessMessage
from app.core.status_codes import StatusCode

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("", response_model=BaseResponse[list[JobResponse]])
def get_jobs(db: Session = Depends(get_db)):
    jobs = get_jobs_service(db)
    return BaseResponse(
        success=True,
        status_code=StatusCode.OK,
        message=SuccessMessage.JOBS_RETRIEVED,
        data=jobs
    )


@router.post("", response_model=BaseResponse[JobResponse],
    status_code=StatusCode.CREATED)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    created_job = create_job_service(db, job_data)
    return BaseResponse(
        success=True,
        status_code=StatusCode.CREATED,
        message=SuccessMessage.JOB_CREATED,
        data=created_job
    )

@router.get("/{job_id}", response_model=BaseResponse[JobResponse])
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    found_job = get_by_id_service(db, job_id)
    return BaseResponse(
        success=True,
        status_code=StatusCode.OK,
        message=SuccessMessage.JOB_RETRIEVED,
        data=found_job
    )