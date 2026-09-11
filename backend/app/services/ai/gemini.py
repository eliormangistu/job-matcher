from app.core.config import GEMINI_MODELS, GEMINI_API_KEY
from app.core.exceptions import GeminiException
from app.core import ErrorMessage, StatusCode
from app.core.logger import logger

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError


client = genai.Client(api_key=GEMINI_API_KEY)


def gemini_generate_content(contents, response_schema):

    for attempt, model in enumerate(GEMINI_MODELS, start=1):
        logger.info(
            "Gemini request started",
            extra={
                "service": "gemini",
                "action": "generate_content",
                "model": model,
                "attempt": attempt,
            },
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
                extra={
                    "service": "gemini",
                    "action": "generate_content",
                    "model": model,
                    "attempt": attempt,
                },
            )

            return response

        except ClientError as exc:
            status_code = getattr(exc, "status_code", None)

            logger.warning(
                "Gemini client error",
                extra={
                    "service": "gemini",
                    "action": "generate_content",
                    "model": model,
                    "status_code": status_code,
                    "attempt": attempt,
                },
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
                extra={
                    "service": "gemini",
                    "action": "generate_content",
                    "model": model,
                    "status_code": status_code,
                    "attempt": attempt,
                },
            )

            # Try the next model.
            continue

        except Exception as exc:
            logger.exception(
                "Unexpected Gemini error",
                extra={
                    "service": "gemini",
                    "action": "generate_content",
                    "model": model,
                    "attempt": attempt,
                },
            )

            raise GeminiException(
                "Gemini service is temporarily unavailable.",
                StatusCode.INTERNAL_SERVER_ERROR,
            ) from exc

    logger.error(
        "All Gemini models failed",
        extra={
            "service": "gemini",
            "action": "generate_content",
            "models": GEMINI_MODELS,
            "attempt": attempt,
        },
    )

    raise GeminiException(
        ErrorMessage.AI_SERVICE_UNAVAILABLE,
        StatusCode.SERVICE_UNAVAILABLE,
    )
