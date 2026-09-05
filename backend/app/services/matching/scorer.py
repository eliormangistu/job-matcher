from app.models import Job
from app.schemas.cv import CandidateProfile
from app.services.matching import rules

SKILL_WEIGHT = 50
EXPERIENCE_WEIGHT = 20
ROLE_WEIGHT = 15
LANGUAGE_WEIGHT = 10
EDUCATION_WEIGHT = 5


def score(candidate: CandidateProfile, job: Job, matched_skills: list[str]) -> float:
    total = 0.0

    if candidate.skills:
        total += SKILL_WEIGHT * len(matched_skills) / len(candidate.skills)
    if rules.experience_matches(candidate, job):
        total += EXPERIENCE_WEIGHT
    if rules.role_matches(candidate, job):
        total += ROLE_WEIGHT
    if rules.languages_match(candidate, job):
        total += LANGUAGE_WEIGHT
    if rules.education_matches(candidate, job):
        total += EDUCATION_WEIGHT

    return round(total, 2)
