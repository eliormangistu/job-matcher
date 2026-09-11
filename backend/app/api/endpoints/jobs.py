from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import JobResponse, JobsResponse
from app.services import (
    get_jobs as get_jobs_service,
    get_by_id as get_by_id_service,
)
from app.schemas import BaseResponse
from app.core import SuccessMessage, StatusCode


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=BaseResponse[JobsResponse])
def get_jobs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    jobs, total = get_jobs_service(
        db,
        limit=limit,
        offset=offset,
    )

    return BaseResponse(
        True,
        StatusCode.OK,
        SuccessMessage.JOBS_RETRIEVED,
        JobsResponse(
            items=jobs,
            total=total,
        ),
    )


@router.get("/{job_id}", response_model=BaseResponse[JobResponse])
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    found_job = get_by_id_service(db, job_id)

    return BaseResponse(True, StatusCode.OK, SuccessMessage.JOB_RETRIEVED, found_job)
