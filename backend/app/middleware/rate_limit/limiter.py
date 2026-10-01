from fastapi import Request
from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import RATE_LIMIT, RATE_LIMIT_WINDOW_SECONDS
from app.core.logger import ServiceLogger
from app.middleware.client_ip import get_client_ip

logger = ServiceLogger("rate_limit")


def is_allowed(client_id: str) -> bool:

    key = f"rate_limit:{client_id}"

    try:
        current_count = redis_client.incr(key)

        if current_count == 1:
            redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)

    except RedisError:
        logger.warning(
            "Redis unavailable, skipping rate limit",
            action="is_allowed",
        )
        return True

    allowed = current_count <= RATE_LIMIT

    logger.info(
        "Rate limit checked",
        action="is_allowed",
        count=current_count,
        limit=RATE_LIMIT,
        allowed=allowed,
    )

    if not allowed:
        logger.warning(
            "Rate limit exceeded",
            action="is_allowed",
            count=current_count,
            limit=RATE_LIMIT,
        )

    return allowed


def is_login_allowed(
    request: Request,
    email: str,
    device_id: str,
) -> bool:
    client_ip = get_client_ip(request)
    normalized_email = email.strip().lower()

    limits = [
        (f"login:ip:{client_ip}", 5),
        (f"login:email:{normalized_email}", 5),
        (f"login:device:{device_id}", 10),
    ]

    for key, limit in limits:
        try:
            current_count = redis_client.incr(key)

            if current_count == 1:
                redis_client.expire(key, 60)

            if current_count > limit:
                logger.warning(
                    "Login rate limit exceeded",
                    action="is_login_allowed",
                    limit=limit,
                )
                return False

        except RedisError:
            logger.warning(
                "Redis unavailable, skipping login rate limit",
                action="is_login_allowed",
            )
            return True

    return True
