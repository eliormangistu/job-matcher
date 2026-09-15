from time import time

from app.core.config import CONTENT_CACHE_TTL_SECONDS
from app.core.logger import ServiceLogger
from app.services.contentful import get_all_content

logger = ServiceLogger("content-cache")

_CACHE: dict | None = None
_CACHE_EXPIRES_AT = 0.0


def get_content() -> dict:
    global _CACHE
    global _CACHE_EXPIRES_AT

    now = time()

    if _CACHE is not None and now < _CACHE_EXPIRES_AT:
        logger.info(
            "Returning content from cache",
            action="cache_hit",
        )
        return _CACHE

    logger.info(
        "Content cache miss",
        action="cache_miss",
    )

    content = get_all_content()

    _CACHE = content
    _CACHE_EXPIRES_AT = now + CONTENT_CACHE_TTL_SECONDS

    logger.info(
        "Content cache updated",
        action="cache_updated",
    )

    return _CACHE


def invalidate_content() -> None:
    global _CACHE
    global _CACHE_EXPIRES_AT

    _CACHE = None
    _CACHE_EXPIRES_AT = 0.0

    logger.info(
        "Content cache invalidated",
        action="cache_invalidated",
    )
