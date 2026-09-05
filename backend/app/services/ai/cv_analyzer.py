from google import genai
from google.genai import types

from app.core.config import GEMINI_API_KEY
from app.schemas.cv import CVProfile


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def analyze_cv_pdf(pdf_path: str) -> CVProfile:
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf_data,
                mime_type="application/pdf",
            ),
            """
Analyze this CV and extract the candidate's professional profile.

Return:
- professional summary
- technical skills
- relevant job titles
- years of professional experience
- education
- languages
- industries

Use only information that appears in the CV.
""",
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CVProfile,
        ),
    )

    return CVProfile.model_validate_json(response.text)