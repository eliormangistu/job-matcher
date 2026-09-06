from app.models import Job
from app.schemas import JobResponse
from app.schemas.job import JobAnalysisRequest
from app.schemas.match import JobMatch
from app.schemas.cv import CvCandidateProfile
from app.services.matching import rules
from app.services.matching.scorer import score
from app.services.ai.job_analyzer import analyze_jobs
from app.core.logger import logger


def match(
    candidate: CvCandidateProfile,
    job: Job,
) -> JobMatch:

    matched_skills, missing_skills = rules.skill_matches(
        candidate,
        job,
    )

    result = JobMatch(
        job_id=job.id,
        score=score(candidate, job, matched_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        job=JobResponse.model_validate(
            job,
            from_attributes=True,
        ),
    )

    logger.info(
        "Job match calculated",
        extra={
            "service": "matcher",
            "action": "match",
            "job_id": job.id,
            "score": result.score,
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
        },
    )

    return result


def rank_jobs(
    candidate: CvCandidateProfile,
    jobs: list[Job],
    limit: int = 10,
) -> list[JobMatch]:

    logger.info(
        "Job matching started",
        extra={
            "service": "matcher",
            "action": "rank_jobs",
            "jobs_count": len(jobs),
            "limit": limit,
        },
    )

    eligible_jobs = []

    for job in jobs:
        if not rules.role_matches(candidate, job):
            continue

        if not rules.experience_matches(candidate, job):
            continue

        if not rules.languages_match(candidate, job):
            continue

        if not rules.education_matches(candidate, job):
            continue

        eligible_jobs.append(job)

    logger.info(
        "Job eligibility filtering completed",
        extra={
            "service": "matcher",
            "action": "filter_jobs",
            "input_jobs_count": len(jobs),
            "eligible_jobs_count": len(eligible_jobs),
        },
    )

    if not eligible_jobs:
        logger.info(
            "No eligible jobs found",
            extra={
                "service": "matcher",
                "action": "rank_jobs",
            },
        )
        return []

    job_inputs = [
        JobAnalysisRequest(
            job_id=job.id,
            requirements=job.requirements or "",
        )
        for job in eligible_jobs
    ]

    logger.info(
        "Job AI analysis started",
        extra={
            "service": "matcher",
            "action": "analyze_jobs",
            "eligible_jobs_count": len(eligible_jobs),
        },
    )

    job_analyses = analyze_jobs(job_inputs)

    logger.info(
        "Job AI analysis completed",
        extra={
            "service": "matcher",
            "action": "analyze_jobs",
            "results_count": len(job_analyses.jobs),
        },
    )

    analyses_by_job_id = {item.job_id: item for item in job_analyses.jobs}

    matches = []

    for job in eligible_jobs:
        analysis = analyses_by_job_id.get(job.id)

        if analysis is None:
            logger.warning(
                "Job analysis missing",
                extra={
                    "service": "matcher",
                    "action": "process_analysis",
                    "job_id": job.id,
                },
            )
            continue

        job.required_skills = analysis.required_skills

        result = match(candidate, job)

        if result is not None:
            matches.append(result)

    relevant_matches = [result for result in matches if result.score > 0]

    ranked_matches = sorted(
        relevant_matches,
        key=lambda result: result.score,
        reverse=True,
    )[:limit]

    logger.info(
        "Job matching completed",
        extra={
            "service": "matcher",
            "action": "rank_jobs",
            "eligible_jobs_count": len(eligible_jobs),
            "matches_count": len(matches),
            "relevant_matches_count": len(relevant_matches),
            "returned_matches_count": len(ranked_matches),
        },
    )

    return ranked_matches
