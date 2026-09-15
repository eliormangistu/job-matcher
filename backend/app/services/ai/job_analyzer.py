from app.schemas.job import JobAnalysisBatch, JobAnalysisRequest

from app.core.logger import ServiceLogger
from .gemini import gemini_generate_content


logger = ServiceLogger("job_analyzer")


def analyze_jobs(
    jobs: list[JobAnalysisRequest],
) -> JobAnalysisBatch:
    logger.info(
        "Job AI analysis started",
        action="analyze_jobs",
        jobs_count=len(jobs),
    )

    jobs_text = "\n\n".join(
        f"""
Job ID: {job.job_id}

Job requirements:

{job.requirements or ""}
"""
        for job in jobs
    )

    logger.info(
        "Job AI prompt prepared",
        action="prepare_prompt",
        jobs_count=len(jobs),
    )

    try:
        response = gemini_generate_content(
            contents=[
                f"""
Analyze the following job requirements.

For each job, extract the required technical and professional skills.

Return one result for every Job ID.

Return only skills that are explicitly required, mentioned as requirements,
or clearly stated as bonus skills.

Do not include:

- company names
- job titles
- industries
- general descriptions
- responsibilities that are not skills

Normalize skill names where appropriate.

For example:

- K8s → Kubernetes
- GCP → Google Cloud Platform

Jobs:

{jobs_text}
"""
            ],
            response_schema=JobAnalysisBatch,
        )

        result = JobAnalysisBatch.model_validate_json(response.text)

        logger.info(
            "Job AI analysis completed",
            action="analyze_jobs",
            jobs_count=len(jobs),
            results_count=len(result.jobs),
        )

        return result

    except Exception:
        logger.exception(
            "Job AI analysis failed",
            action="analyze_jobs",
            jobs_count=len(jobs),
        )
        raise
