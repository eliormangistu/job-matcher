import json
from pathlib import Path
from unittest.mock import Mock, patch

from app.services.ai.cv_analyzer import analyze_cv_pdf


MOCK_CV_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "mock_cv_response.json"
)


def test_analyze_cv_pdf(tmp_path):

    fake_pdf = tmp_path / "fake_cv.pdf"
    fake_pdf.write_bytes(b"fake pdf content")

    with open(MOCK_CV_PATH, "r", encoding="utf-8") as file:
        mock_data = json.load(file)

    mock_response = Mock()
    mock_response.text = json.dumps(mock_data)

    with patch(
        "app.services.ai.cv_analyzer.client.models.generate_content",
        return_value=mock_response
    ):
        profile = analyze_cv_pdf(str(fake_pdf))

    assert profile.summary == mock_data["summary"]
    assert profile.skills == mock_data["skills"]
    assert profile.job_titles == mock_data["job_titles"]
    assert profile.years_of_experience == mock_data["years_of_experience"]
    assert profile.education == mock_data["education"]
    assert profile.languages == mock_data["languages"]
    assert profile.industries == mock_data["industries"]