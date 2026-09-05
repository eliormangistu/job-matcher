import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.services.ai.cv_analyzer import analyze_cv_pdf


async def process_cv(file: UploadFile):
    pdf_data = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(pdf_data)
        temp_path = temp_file.name

    try:
        return analyze_cv_pdf(temp_path)
    finally:
        Path(temp_path).unlink(missing_ok=True)
