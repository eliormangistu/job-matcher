from app.core.config import GEMINI_MODELS, GEMINI_API_KEY
from app.core.exceptions import GeminiException
from app.core import ErrorMessage, StatusCode
from app.core.logger import ServiceLogger

from google import genai
from app.schemas.cv import CvCandidateProfile
from google.genai import types
from google.genai.errors import ClientError, ServerError
from app.services.prompts.cv import CV_ANALYSIS_PROMPT

logger = ServiceLogger("gemini")

client = genai.Client(api_key=GEMINI_API_KEY)


def gemini_generate_content(contents, response_schema):
    for attempt, model in enumerate(GEMINI_MODELS, start=1):
        logger.info(
            "Gemini request started",
            action="generate_content",
            model=model,
            attempt=attempt,
        )

        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                ),
            )

            logger.info(
                "Gemini request completed",
                action="generate_content",
                model=model,
                attempt=attempt,
            )

            return response

        except ClientError as exc:
            status_code = getattr(exc, "status_code", None)

            logger.warning(
                "Gemini client error",
                action="generate_content",
                model=model,
                status_code=status_code,
                attempt=attempt,
            )

            # Quota / rate limit
            if status_code == StatusCode.TOO_MANY_REQUESTS:
                continue

            # Errors such as 400, 401, 403 should not blindly
            # trigger fallback to another model.
            raise GeminiException(
                "Gemini request failed.",
                StatusCode.INTERNAL_SERVER_ERROR,
            ) from exc

        except ServerError as exc:
            status_code = getattr(exc, "status_code", None)

            logger.warning(
                "Gemini server error - trying next model",
                action="generate_content",
                model=model,
                status_code=status_code,
                attempt=attempt,
            )

            # Try the next model.
            continue

        except Exception as exc:
            logger.exception(
                "Unexpected Gemini error",
                action="generate_content",
                model=model,
                attempt=attempt,
            )

            raise GeminiException(
                "Gemini service is temporarily unavailable.",
                StatusCode.INTERNAL_SERVER_ERROR,
            ) from exc

    logger.error(
        "All Gemini models failed",
        action="generate_content",
        models=GEMINI_MODELS,
        attempt=attempt,
    )

    raise GeminiException(
        ErrorMessage.AI_SERVICE_UNAVAILABLE,
        StatusCode.SERVICE_UNAVAILABLE,
    )


def analyze_cv_with_gemini(
    pdf_data: bytes,
) -> CvCandidateProfile:
    logger.info(
        "Sending CV to Gemini",
        action="gemini_request",
    )

    response = gemini_generate_content(
        contents=[
            types.Part.from_bytes(
                data=pdf_data,
                mime_type="application/pdf",
            ),
            CV_ANALYSIS_PROMPT,
        ],
        response_schema=CvCandidateProfile,
    )

    logger.info(
        "Gemini CV analysis completed",
        action="gemini_request",
    )

    return CvCandidateProfile.model_validate_json(
        response.text,
    )
