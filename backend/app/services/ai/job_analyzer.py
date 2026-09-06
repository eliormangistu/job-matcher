from app.schemas.job import JobAnalysis
from .gemini import gemini_generate_content


def analyze_job(requirements: str) -> JobAnalysis:
    response = gemini_generate_content(
        contents=[
            f"""
Analyze the following job requirements and extract the required technical
and professional skills.

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

Job requirements:
{requirements}
""",
        ],
        response_schema=JobAnalysis,
    )

    return JobAnalysis.model_validate_json(response.text)
