from google.genai import types

from app.schemas.cv import CvCandidateProfile
from app.core.logger import logger

from .gemini import gemini_generate_content


def analyze_cv_pdf(pdf_path: str) -> CvCandidateProfile:
    logger.info(
        "CV PDF analysis started",
        extra={
            "service": "cv_analyzer",
            "action": "analyze_cv_pdf",
        },
    )

    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        logger.info(
            "CV PDF loaded",
            extra={
                "service": "cv_analyzer",
                "action": "load_pdf",
                "size_bytes": len(pdf_data),
            },
        )

        logger.info(
            "Sending CV to Gemini",
            extra={
                "service": "cv_analyzer",
                "action": "gemini_request",
            },
        )

        response = gemini_generate_content(
            contents=[
                types.Part.from_bytes(
                    data=pdf_data,
                    mime_type="application/pdf",
                ),
                """
Analyze this CV and extract the candidate's professional profile.

Return:

- professional summary
- technical skills
- relevant job titles
- years of professional experience
- education
- languages
- industries

Use only information that appears in the CV.

""",
            ],
            response_schema=CvCandidateProfile,
        )

        logger.info(
            "Gemini CV analysis completed",
            extra={
                "service": "cv_analyzer",
                "action": "gemini_request",
            },
        )

        result = CvCandidateProfile.model_validate_json(response.text)

        logger.info(
            "CV profile parsed successfully",
            extra={
                "service": "cv_analyzer",
                "action": "parse_response",
            },
        )

        return result

    except Exception:
        logger.exception(
            "CV analysis failed",
            extra={
                "service": "cv_analyzer",
                "action": "analyze_cv_pdf",
            },
        )
        raise
