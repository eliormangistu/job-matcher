from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import RATE_LIMIT, RATE_LIMIT_WINDOW_SECONDS
from app.core.logger import logger


def is_allowed(client_id: str) -> bool:
    key = f"rate_limit:{client_id}"

    try:
        current_count = redis_client.incr(key)

        if current_count == 1:
            redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)

    except RedisError:
        logger.warning(
            "Redis unavailable, skipping rate limit",
            extra={
                "service": "rate_limit",
                "action": "is_allowed",
            },
        )
        return True

    allowed = current_count <= RATE_LIMIT

    logger.info(
        "Rate limit checked",
        extra={
            "service": "rate_limit",
            "action": "is_allowed",
            "count": current_count,
            "limit": RATE_LIMIT,
            "allowed": allowed,
        },
    )

    if not allowed:
        logger.warning(
            "Rate limit exceeded",
            extra={
                "service": "rate_limit",
                "action": "is_allowed",
                "count": current_count,
                "limit": RATE_LIMIT,
            },
        )

    return allowed
