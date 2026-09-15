import tempfile

from pathlib import Path

from fastapi import UploadFile

from app.core.logger import ServiceLogger
from app.services.ai.cv_analyzer import analyze_cv_pdf


logger = ServiceLogger("cv")


async def process_cv(file: UploadFile):
    logger.info(
        "CV processing started",
        action="process_cv",
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
        Path(temp_path).unlink(missing_ok=True)

        logger.info(
            "CV temporary file deleted",
            action="cleanup",
        )
