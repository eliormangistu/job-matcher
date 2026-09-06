import logging

from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import RATE_LIMIT, RATE_LIMIT_WINDOW_SECONDS

logger = logging.getLogger("job-matcher")


def is_allowed(client_id: str) -> bool:
    key = f"rate_limit:{client_id}"

    try:
        current_count = redis_client.incr(key)
        if current_count == 1:
            redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)
    except RedisError:
        logger.warning("Redis unavailable, skipping rate limit")
        return True

    return current_count <= RATE_LIMIT
