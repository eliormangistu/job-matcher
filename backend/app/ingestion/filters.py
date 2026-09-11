from app.core.config import (
    ALLOWED_JOB_FIELDS,
    MAX_JOB_EXPERIENCE,
)


def is_allowed_field(field: str | None) -> bool:
    return field in ALLOWED_JOB_FIELDS


def is_allowed_experience(min_experience) -> bool:
    if min_experience is None:
        return True

    try:
        return int(min_experience) <= MAX_JOB_EXPERIENCE
    except (ValueError, TypeError):
        return True
