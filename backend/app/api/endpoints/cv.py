from app.schemas.match import JobMatch
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.services.cv import process_cv, create_cv, get_by_user_id, get_user_cv
from app.services.matching.matcher import rank_jobs
from app.services.auth import verify_access_token
from app.db.session import get_db
from app.repositories.job import get_all_for_matching
from app.schemas import BaseResponse, CVUploadData
from app.schemas.responses.cv import CVResponse
from app.core import SuccessMessage, StatusCode
from app.services.cv_match import (
    save_matches,
    get_job_matches_for_cv,
    refresh_matches_for_cv,
)
from app.core.security.csrf import require_csrf_token


router = APIRouter(prefix="/cv", tags=["cv"])


@router.post(
    "/upload_cv",
    response_model=BaseResponse[CVUploadData],
)
async def upload_cv(
    file: UploadFile = File(...),
    user=Depends(verify_access_token),
    _: None = Depends(require_csrf_token),
    db: Session = Depends(get_db),
):
    profile = await process_cv(file)

    cv = create_cv(
        db=db,
        user_id=user.id,
        filename=file.filename,
        file_type=file.content_type or "application/pdf",
        content=None,
        profile=profile,
    )

    matches = rank_jobs(
        profile,
        get_all_for_matching(db),
    )

    save_matches(
        db=db,
        cv_id=cv.id,
        matches=matches,
    )

    return BaseResponse[CVUploadData](
        True,
        StatusCode.OK,
        SuccessMessage.CV_UPLOADED,
        CVUploadData(
            filename=file.filename,
            profile=profile,
            matches=matches,
        ),
    )


@router.get(
    "/get_cv",
    response_model=BaseResponse[CVResponse | None],
)
def get_cv(
    user=Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    cv = get_by_user_id(
        db=db,
        user_id=user.id,
    )

    return BaseResponse[CVResponse | None](
        True,
        StatusCode.OK,
        SuccessMessage.CV_FETCHED,
        cv,
    )


@router.get(
    "/get_matches",
    response_model=BaseResponse[list[JobMatch]],
)
def get_matches(
    user=Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    cv = get_user_cv(
        db=db,
        user_id=user.id,
    )

    if cv is None:
        return BaseResponse[list[JobMatch]](
            True,
            StatusCode.OK,
            SuccessMessage.CV_MATCHES_FETCHED,
            [],
        )

    matches = get_job_matches_for_cv(
        db=db,
        cv_id=cv.id,
    )

    return BaseResponse[list[JobMatch]](
        True,
        StatusCode.OK,
        SuccessMessage.CV_MATCHES_FETCHED,
        matches,
    )


@router.post(
    "/refresh_matches",
    response_model=BaseResponse[list[JobMatch]],
)
def refresh_matches(
    user=Depends(verify_access_token),
    _: None = Depends(require_csrf_token),
    db: Session = Depends(get_db),
):
    cv = get_user_cv(
        db=db,
        user_id=user.id,
    )

    if cv is None:
        return BaseResponse[list[JobMatch]](
            True,
            StatusCode.OK,
            SuccessMessage.CV_MATCHES_FETCHED,
            [],
        )

    refresh_matches_for_cv(
        db=db,
        cv_id=cv.id,
    )

    matches = get_job_matches_for_cv(
        db=db,
        cv_id=cv.id,
    )

    return BaseResponse[list[JobMatch]](
        True,
        StatusCode.OK,
        SuccessMessage.CV_MATCHES_FETCHED,
        matches,
    )
