from app.models import Job
from app.schemas import CandidateProfile, JobResponse, MatchResult
from app.services.matching import rules
from app.services.matching.scorer import score


def match(candidate: CandidateProfile, job: Job) -> MatchResult:
    matched_skills, missing_skills = rules.skill_matches(candidate, job)

    return MatchResult(
        job_id=job.id,
        score=score(candidate, job, matched_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        job=JobResponse.model_validate(job, from_attributes=True),
    )


def rank_jobs(
    candidate: CandidateProfile,
    jobs: list[Job],
    limit: int = 10,
) -> list[MatchResult]:
    matches = [match(candidate, job) for job in jobs]
    relevant_matches = [result for result in matches if result.score > 0]
    return sorted(relevant_matches, key=lambda result: result.score, reverse=True)[:limit]
