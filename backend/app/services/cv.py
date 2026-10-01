import tempfile
from app.validations.files import (
    validate_cv_content_type,
    validate_cv_file_size,
    validate_cv_filename,
    validate_pdf_signature,
)
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi import UploadFile
from app.models.cv import CV
from app.repositories.cv import create, get_by_user_id
from app.repositories.cv_match import get_latest_by_user_id, update
from app.schemas.cv import CvCandidateProfile
from app.core.logger import ServiceLogger
from app.services.ai.cv_analyzer import analyze_cv_pdf


logger = ServiceLogger("cv")


async def process_cv(file: UploadFile):
    logger.info(
        "CV processing started",
        action="process_cv",
    )

    validate_cv_filename(
        filename=file.filename,
    )

    validate_cv_content_type(
        content_type=file.content_type,
    )

    await validate_cv_file_size(
        file=file,
    )

    await validate_pdf_signature(
        file=file,
    )

    pdf_data = await file.read()

    logger.info(
        "CV file read",
        action="read_file",
        size_bytes=len(pdf_data),
    )

    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False,
    ) as temp_file:
        temp_file.write(pdf_data)
        temp_path = temp_file.name

    try:
        logger.info(
            "CV analysis started",
            action="analyze_cv",
        )

        result = analyze_cv_pdf(temp_path)

        logger.info(
            "CV analysis completed",
            action="analyze_cv",
        )

        return result

    except Exception:
        logger.exception(
            "CV processing failed",
            action="process_cv",
        )
        raise

    finally:
        Path(temp_path).unlink(
            missing_ok=True,
        )

        logger.info(
            "CV temporary file deleted",
            action="cleanup",
        )


def create_cv(
    db: Session,
    user_id: int,
    filename: str,
    file_type: str,
    content: str | None,
    profile: CvCandidateProfile,
) -> CV:
    logger.info(
        "Creating or updating CV",
        action="create_or_update_cv",
        user_id=user_id,
        cv_filename=filename,
    )

    cv = get_latest_by_user_id(
        db=db,
        user_id=user_id,
    )

    if cv is None:
        cv = CV(
            user_id=user_id,
            filename=filename,
            file_type=file_type,
            content=content,
            summary=profile.summary,
            skills=profile.skills,
            job_titles=profile.roles,
            years_of_experience=profile.years_of_experience,
            education=profile.education,
            languages=profile.languages,
            industries=profile.industries,
        )

        cv = create(
            db=db,
            cv=cv,
        )

        logger.info(
            "New CV created",
            action="create_or_update_cv",
            cv_id=cv.id,
            user_id=user_id,
        )

        return cv

    cv.filename = filename
    cv.file_type = file_type
    cv.content = content
    cv.summary = profile.summary
    cv.skills = profile.skills
    cv.job_titles = profile.roles
    cv.years_of_experience = profile.years_of_experience
    cv.education = profile.education
    cv.languages = profile.languages
    cv.industries = profile.industries

    cv = update(
        db=db,
        cv=cv,
    )

    logger.info(
        "Existing CV updated",
        action="create_or_update_cv",
        cv_id=cv.id,
        user_id=user_id,
    )

    return cv


def get_user_cv(
    db: Session,
    user_id: int,
) -> CV | None:
    logger.info(
        "Fetching user CV",
        action="get_user_cv",
        user_id=user_id,
    )

    cv = get_by_user_id(
        db=db,
        user_id=user_id,
    )

    logger.info(
        "User CV fetched successfully",
        action="get_user_cv",
        user_id=user_id,
        found=cv is not None,
    )

    return cv


def build_candidate_profile(cv: CV) -> CvCandidateProfile:
    logger.info(
        "Building candidate profile from CV",
        action="build_candidate_profile",
        cv_id=cv.id,
    )

    return CvCandidateProfile(
        summary=cv.summary,
        skills=cv.skills,
        roles=cv.job_titles,
        years_of_experience=cv.years_of_experience,
        education=cv.education,
        languages=cv.languages,
        industries=cv.industries,
    )
