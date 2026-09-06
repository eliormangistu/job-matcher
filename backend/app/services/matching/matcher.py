from app.models import Job
from app.schemas import JobResponse
from app.schemas.match import JobMatch
from app.schemas.cv import CvCandidateProfile
from app.services.ai.job_analyzer import analyze_job
from app.services.matching import rules
from app.services.matching.scorer import score


def match(candidate: CvCandidateProfile, job: Job) -> JobMatch | None:
    if not rules.role_matches(candidate, job):
        return None

    if not rules.experience_matches(candidate, job):
        return None

    if not rules.languages_match(candidate, job):
        return None

    if not rules.education_matches(candidate, job):
        return None

    job_analysis = analyze_job(job.requirements or "")
    job.required_skills = job_analysis.required_skills

    matched_skills, missing_skills = rules.skill_matches(candidate, job)

    return JobMatch(
        job_id=job.id,
        score=score(candidate, job, matched_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        job=JobResponse.model_validate(job, from_attributes=True),
    )


def rank_jobs(
    candidate: CvCandidateProfile,
    jobs: list[Job],
    limit: int = 10,
) -> list[JobMatch]:

    matches = [result for job in jobs if (result := match(candidate, job)) is not None]

    relevant_matches = [result for result in matches if result.score > 0]

    return sorted(
        relevant_matches,
        key=lambda result: result.score,
        reverse=True,
    )[:limit]
