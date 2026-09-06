import re

from app.models import Job
from app.schemas.cv import CvCandidateProfile


def normalize(value: str) -> str:
    return " ".join(
        re.findall(
            r"[a-z0-9+#.]+",
            value.lower(),
        )
    )


def skill_matches(
    candidate: CvCandidateProfile,
    job: Job,
) -> tuple[list[str], list[str]]:

    candidate_skills = {
        normalize(skill): skill for skill in candidate.skills if normalize(skill)
    }

    required_skills = {
        normalize(skill): skill for skill in job.required_skills if normalize(skill)
    }

    matched = [
        candidate_skills[skill]
        for skill in candidate_skills
        if skill in required_skills
    ]

    missing = [
        required_skills[skill]
        for skill in required_skills
        if skill not in candidate_skills
    ]

    return matched, missing


def role_matches(
    candidate: CvCandidateProfile,
    job: Job,
) -> bool:

    normalized_job_title = normalize(job.title)

    return any(
        (normalized_role := normalize(role))
        and (
            normalized_role in normalized_job_title
            or normalized_job_title in normalized_role
        )
        for role in candidate.roles
    )


def experience_matches(
    candidate: CvCandidateProfile,
    job: Job,
) -> bool:

    return job.min_experience is None or (
        candidate.years_of_experience is not None
        and candidate.years_of_experience >= job.min_experience
    )


def languages_match(
    candidate: CvCandidateProfile,
    job: Job,
) -> bool:

    required_languages = {
        normalize(language) for language in job.language_requirement or []
    }

    candidate_languages = {normalize(language) for language in candidate.languages}

    return not required_languages or bool(required_languages & candidate_languages)


def education_matches(
    candidate: CvCandidateProfile,
    job: Job,
) -> bool:

    if not job.education_requirements:
        return True

    requirements = normalize(job.education_requirements)

    return any(
        normalize(education) in requirements for education in candidate.education
    )
