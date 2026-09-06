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
from app.services.ai.job_analyzer import analyze_job


@pytest.mark.integration
def test_analyze_job():
    requirements = """
    3+ years of experience with Python and FastAPI.
    Experience with PostgreSQL and Docker.
    """

    result = analyze_job(requirements)

    assert result.required_skills
    assert "Python" in result.required_skills
