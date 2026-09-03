import time

from app.cache.redis import redis_client
from app.core.config import (
    RATE_LIMIT,
    RATE_LIMIT_WINDOW_SECONDS
)


def is_allowed(client_id: str) -> bool:
    key = f"rate_limit:{client_id}"

    current_count = redis_client.get(key)

    if current_count is None:
        redis_client.set(
            key,
            1,
            ex=RATE_LIMIT_WINDOW_SECONDS
        )
        return True

    if int(current_count) >= RATE_LIMIT:
        return False

    redis_client.incr(key)

    return True