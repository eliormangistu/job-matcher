from google.genai import types

from app.schemas.cv import CvCandidateProfile
from app.core.logger import ServiceLogger
from .gemini import analyze_cv_with_gemini


logger = ServiceLogger("cv_analyzer")


def analyze_cv_pdf(
    pdf_path: str,
) -> CvCandidateProfile:
    logger.info(
        "CV PDF analysis started",
        action="analyze_cv_pdf",
    )

    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        logger.info(
            "CV PDF loaded",
            action="load_pdf",
            size_bytes=len(pdf_data),
        )

        result = analyze_cv_with_gemini(
            pdf_data=pdf_data,
        )

        logger.info(
            "CV profile parsed successfully",
            action="parse_response",
        )

        return result

    except Exception:
        logger.exception(
            "CV analysis failed",
            action="analyze_cv_pdf",
        )
        raise
