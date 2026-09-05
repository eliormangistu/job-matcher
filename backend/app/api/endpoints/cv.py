from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.services.cv import process_cv
from app.services.matching.matcher import rank_jobs
from app.services.auth import verify_user
from app.db.session import get_db
from app.repositories import job as job_repository
from app.schemas import BaseResponse, CVUploadData
from app.core import SuccessMessage, StatusCode

router = APIRouter()


@router.post("/cv", response_model=BaseResponse[CVUploadData])
async def upload_cv(
    file: UploadFile = File(...),
    user=Depends(verify_user),
    db: Session = Depends(get_db),
):
    profile = await process_cv(file)
    matches = rank_jobs(profile, job_repository.get_all_for_matching(db))

    return BaseResponse(
        True,
        StatusCode.OK,
        SuccessMessage.CV_UPLOADED,
        CVUploadData(
            filename=file.filename,
            profile=profile,
            matches=matches,
        ),
    )
