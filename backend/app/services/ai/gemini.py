from app.core.config import GEMINI_MODEL, GEMINI_API_KEY
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)


def gemini_generate_content(contents, response_schema):
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    return response
