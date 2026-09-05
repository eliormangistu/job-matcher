import re

from app.models import Job
from app.schemas.cv import CandidateProfile


def normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9+#.]+", value.lower()))


def job_text(job: Job) -> str:
    values = [
        job.title,
        job.field,
        job.description,
        job.requirements,
        job.education_requirements,
        " ".join(job.company_industry or []),
        " ".join(job.language_requirement or []),
    ]
    return normalize(" ".join(value for value in values if value))


def skill_matches(candidate: CandidateProfile, job: Job) -> tuple[list[str], list[str]]:
    text = job_text(job)
    matched = [
        skill
        for skill in candidate.skills
        if (normalized_skill := normalize(skill)) and normalized_skill in text
    ]
    missing = [skill for skill in candidate.skills if skill not in matched]
    return matched, missing


def role_matches(candidate: CandidateProfile, job: Job) -> bool:
    normalized_job_title = normalize(job.title)
    return any(
        (normalized_role := normalize(role))
        and (
            normalized_role in normalized_job_title
            or normalized_job_title in normalized_role
        )
        for role in candidate.roles
    )


def experience_matches(candidate: CandidateProfile, job: Job) -> bool:
    return (
        job.min_experience is None
        or (
            candidate.years_of_experience is not None
            and candidate.years_of_experience >= job.min_experience
        )
    )


def languages_match(candidate: CandidateProfile, job: Job) -> bool:
    required_languages = {normalize(language) for language in job.language_requirement or []}
    candidate_languages = {normalize(language) for language in candidate.languages}
    return not required_languages or bool(required_languages & candidate_languages)


def education_matches(candidate: CandidateProfile, job: Job) -> bool:
    if not job.education_requirements:
        return True

    requirements = normalize(job.education_requirements)
    return any(normalize(education) in requirements for education in candidate.education)
