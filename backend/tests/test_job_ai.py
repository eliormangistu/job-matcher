import json
from pathlib import Path
from unittest.mock import Mock, patch

from app.schemas.job import JobAnalysisBatch
from app.services.ai.job_analyzer import analyze_jobs


MOCK_JOB_PATH = Path(__file__).parent.parent / "data" / "mock_job_response.json"


def test_analyze_jobs():
    with open(MOCK_JOB_PATH, "r", encoding="utf-8") as file:
        mock_data = json.load(file)

    mock_response = Mock()
    mock_response.text = json.dumps(
        {
            "jobs": [
                {
                    "job_id": 1,
                    "required_skills": mock_data["required_skills"],
                }
            ]
        }
    )

    with patch(
        "app.services.ai.job_analyzer.gemini_generate_content",
        return_value=mock_response,
    ):
        analysis = analyze_jobs(
            [
                {
                    "job_id": 1,
                    "requirements": (
                        "Backend Engineer with Python, FastAPI and PostgreSQL."
                    ),
                }
            ]
        )

    assert isinstance(analysis, JobAnalysisBatch)
    assert analysis.jobs[0].job_id == 1
    assert analysis.jobs[0].required_skills == mock_data["required_skills"]
