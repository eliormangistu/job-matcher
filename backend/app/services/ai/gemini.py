from app.core.config import GEMINI_MODEL, GEMINI_API_KEY
from app.core.exceptions import GeminiException
from app.core import StatusCode
from app.core.logger import logger

from google import genai
from google.genai import types
from google.genai.errors import ClientError


client = genai.Client(api_key=GEMINI_API_KEY)


def gemini_generate_content(contents, response_schema):
    logger.info(
        "Gemini request started",
        extra={
            "service": "gemini",
            "action": "generate_content",
            "model": GEMINI_MODEL,
        },
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
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
                "model": GEMINI_MODEL,
            },
        )

        return response

    except ClientError as exc:
        if exc.status_code == StatusCode.TOO_MANY_REQUESTS:
            logger.warning(
                "Gemini quota exceeded",
                extra={
                    "service": "gemini",
                    "action": "generate_content",
                    "model": GEMINI_MODEL,
                    "status_code": StatusCode.TOO_MANY_REQUESTS,
                },
            )

            raise GeminiException(
                "Gemini quota exceeded. Please try again later.",
                StatusCode.TOO_MANY_REQUESTS,
            ) from exc

        logger.exception(
            "Gemini client error",
            extra={
                "service": "gemini",
                "action": "generate_content",
                "model": GEMINI_MODEL,
                "status_code": getattr(exc, "status_code", None),
            },
        )

        raise GeminiException(
            "Gemini service is temporarily unavailable",
            StatusCode.INTERNAL_SERVER_ERROR,
        ) from exc

    except Exception:
        logger.exception(
            "Gemini request failed",
            extra={
                "service": "gemini",
                "action": "generate_content",
                "model": GEMINI_MODEL,
            },
        )
        raise
