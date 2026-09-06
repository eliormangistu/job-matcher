import json
from pathlib import Path
from unittest.mock import Mock, patch

from app.schemas.job import JobAnalysis
from app.services.ai.job_analyzer import analyze_job


MOCK_JOB_PATH = Path(__file__).parent.parent / "data" / "mock_job_response.json"


def test_analyze_job():
    with open(MOCK_JOB_PATH, "r", encoding="utf-8") as file:
        mock_data = json.load(file)

    mock_response = Mock()
    mock_response.text = json.dumps(mock_data)

    with patch(
        "app.services.ai.job_analyzer.gemini_generate_content",
        return_value=mock_response,
    ):
        analysis = analyze_job("Backend Engineer with Python, FastAPI and PostgreSQL.")

    assert isinstance(analysis, JobAnalysis)
    assert analysis.required_skills == mock_data["required_skills"]
