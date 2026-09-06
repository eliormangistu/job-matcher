from app.models.job import Job
from app.schemas.cv import CvCandidateProfile
from app.services.matching.matcher import rank_jobs
from unittest.mock import patch
from app.schemas.job import JobAnalysis


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
        min_experience=3,
        required_skills=["Python", "FastAPI", "PostgreSQL"],
    )

    weaker_match = Job(
        id=2,
        airtable_id="match-2",
        title="Frontend Engineer",
        company="Example",
        location=["Tel Aviv"],
        remote=True,
        description="Build user interfaces with Python integrations.",
        min_experience=5,
        required_skills=["Python", "React"],
    )

    with patch(
        "app.services.matching.matcher.analyze_job",
    ) as mock_analyze:
        mock_analyze.return_value = JobAnalysis(
            required_skills=best_match.required_skills
        )

        matches = rank_jobs(profile, [weaker_match, best_match])

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
