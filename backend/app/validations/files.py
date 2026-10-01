from pathlib import Path
from app.core.config import ALLOWED_CV_CONTENT_TYPES
from fastapi import UploadFile
from app.core.config import ALLOWED_CV_EXTENSIONS
from app.core.exceptions import InvalidFileException
from app.core.config import MAX_CV_FILE_SIZE


def validate_cv_filename(
    filename: str | None,
) -> None:
    if not filename:
        raise InvalidFileException()

    path = Path(filename)

    if path.name != filename:
        raise InvalidFileException()

    if path.suffix.lower() not in ALLOWED_CV_EXTENSIONS:
        raise InvalidFileException()


async def validate_cv_file_size(
    file: UploadFile,
) -> None:
    total_size = 0

    while chunk := await file.read(1024 * 1024):
        total_size += len(chunk)

        if total_size > MAX_CV_FILE_SIZE:
            await file.seek(0)
            raise InvalidFileException()

    await file.seek(0)


async def validate_pdf_signature(
    file: UploadFile,
) -> None:
    header = await file.read(5)

    await file.seek(0)

    if header != b"%PDF-":
        raise InvalidFileException()


def validate_cv_content_type(
    content_type: str | None,
) -> None:
    if not content_type:
        raise InvalidFileException()

    if content_type.lower() not in ALLOWED_CV_CONTENT_TYPES:
        raise InvalidFileException()
