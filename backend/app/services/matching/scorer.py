from app.models import Job
from app.schemas.cv import CvCandidateProfile
from app.services.matching import rules
from app.core.config import (
    SKILL_WEIGHT,
    EXPERIENCE_WEIGHT,
    ROLE_WEIGHT,
    LANGUAGE_WEIGHT,
    EDUCATION_WEIGHT,
)


def score(
    candidate: CvCandidateProfile,
    job: Job,
    matched_skills: list[str],
) -> float:
    total = 0.0

    if job.required_skills:
        total += SKILL_WEIGHT * len(matched_skills) / len(job.required_skills)

    if rules.experience_matches(candidate, job):
        total += EXPERIENCE_WEIGHT

    if rules.role_matches(candidate, job):
        total += ROLE_WEIGHT

    if rules.languages_match(candidate, job):
        total += LANGUAGE_WEIGHT

    if rules.education_matches(candidate, job):
        total += EDUCATION_WEIGHT

    return round(total, 2)
