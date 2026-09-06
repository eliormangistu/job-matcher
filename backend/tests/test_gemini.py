# import os

# from dotenv import load_dotenv
# from google import genai

# load_dotenv("env/.env.dev")

# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# response = client.models.generate_content(
#     model="gemini-3.6-flash",
#     contents="Say hello in Hebrew",
# )

# print(response.text)

import pytest
from app.services.ai.job_analyzer import analyze_jobs


@pytest.mark.integration
def test_analyze_jobs():
    requirements = """
    3+ years of experience with Python and FastAPI.

    Experience with PostgreSQL and Docker.
    """

    result = analyze_jobs(
        [
            {
                "job_id": 1,
                "requirements": requirements,
            }
        ]
    )

    assert result.jobs
    assert result.jobs[0].job_id == 1
    assert result.jobs[0].required_skills
    assert "Python" in result.jobs[0].required_skills
