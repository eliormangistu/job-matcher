from unittest.mock import patch

from app.models.job import Job
from app.schemas.cv import CvCandidateProfile
from app.schemas.job import JobAnalysisBatch, JobAnalysisItem
from app.services.matching.matcher import rank_jobs


def test_rank_jobs_orders_the_best_match_first():
    profile = CvCandidateProfile(
        skills=["Python", "FastAPI", "PostgreSQL"],
        roles=["Backend Engineer"],
        years_of_experience=4,
    )

    best_match = Job(
        id=1,
        airtable_id="match-1",
        title="Backend Engineer",
        company="Example",
        location=["Tel Aviv"],
        remote=True,
        description="Build Python and FastAPI services with PostgreSQL.",
        requirements="Python, FastAPI, PostgreSQL",
        min_experience=3,
        required_skills=[],
    )

    weaker_match = Job(
        id=2,
        airtable_id="match-2",
        title="Frontend Engineer",
        company="Example",
        location=["Tel Aviv"],
        remote=True,
        description="Build user interfaces with Python integrations.",
        requirements="Python, React",
        min_experience=5,
        required_skills=[],
    )

    with patch(
        "app.services.matching.matcher.analyze_jobs",
    ) as mock_analyze:
        mock_analyze.return_value = JobAnalysisBatch(
            jobs=[
                JobAnalysisItem(
                    job_id=1,
                    required_skills=["Python", "FastAPI", "PostgreSQL"],
                ),
            ]
        )

        matches = rank_jobs(
            profile,
            [weaker_match, best_match],
        )

        assert [match.job.title for match in matches] == [
            "Backend Engineer",
        ]

        assert matches[0].job_id == 1
        assert matches[0].score == 100
        assert matches[0].matched_skills == [
            "Python",
            "FastAPI",
            "PostgreSQL",
        ]
        assert matches[0].missing_skills == []

        mock_analyze.assert_called_once()
