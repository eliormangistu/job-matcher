from google.genai import types

from app.schemas.cv import CvCandidateProfile
from .gemini import gemini_generate_content


def analyze_cv_pdf(pdf_path: str) -> CvCandidateProfile:
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    response = gemini_generate_content(
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
        response_schema=CvCandidateProfile,
    )

    return CvCandidateProfile.model_validate_json(response.text)
