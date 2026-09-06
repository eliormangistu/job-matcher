import asyncio
import json
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from fastapi import UploadFile

from app.core import SuccessMessage, StatusCode
from app.schemas.cv import CvCandidateProfile
from app.services.cv import process_cv


CV_PATH = Path(__file__).parent.parent / "data" / "mock_cv.pdf"
MOCK_RESPONSE_PATH = Path(__file__).parent.parent / "data" / "mock_cv_response.json"


def test_upload_cv(client):
    with open(MOCK_RESPONSE_PATH, "r", encoding="utf-8") as file:
        mock_data = json.load(file)

    mock_profile = CvCandidateProfile(**mock_data)

    with patch(
        "app.api.endpoints.cv.process_cv",
        return_value=mock_profile,
    ):
        response = client.post(
            "/cv/upload_cv",
            files={
                "file": (
                    "mock_cv.pdf",
                    CV_PATH.read_bytes(),
                    "application/pdf",
                )
            },
        )

    assert response.status_code == StatusCode.OK

    data = response.json()

    assert data["success"] is True
    assert data["status_code"] == StatusCode.OK
    assert data["message"] == SuccessMessage.CV_UPLOADED
    assert data["data"]["filename"] == "mock_cv.pdf"
    assert data["data"]["profile"]["summary"] == mock_data["summary"]
    assert data["data"]["profile"]["skills"] == mock_data["skills"]
    assert data["data"]["matches"] == []


def test_process_cv_removes_temporary_file():
    uploaded_file = UploadFile(
        filename="cv.pdf",
        file=BytesIO(b"fake pdf content"),
    )

    analyzed_paths = []

    def analyze(path):
        analyzed_paths.append(Path(path))
        return CvCandidateProfile(summary="Candidate summary")

    with patch(
        "app.services.cv.analyze_cv_pdf",
        side_effect=analyze,
    ):
        profile = asyncio.run(process_cv(uploaded_file))

    assert profile.summary == "Candidate summary"
    assert not analyzed_paths[0].exists()
