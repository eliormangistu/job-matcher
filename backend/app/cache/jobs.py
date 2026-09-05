import json
import logging

from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import JOBS_CACHE_TTL

logger = logging.getLogger("job-matcher")

JOBS_PAGE_PATTERN = "jobs:page:*"


def get_cache_key(limit: int, offset: int) -> str:
    return f"jobs:page:{offset}:{limit}"


def get_cached_jobs(limit: int, offset: int):
    try:
        cached_jobs = redis_client.get(
            get_cache_key(limit, offset)
        )
    except RedisError:
        logger.warning("Redis unavailable, skipping jobs cache read")
        return None

    if cached_jobs is None:
        return None

    return json.loads(cached_jobs)


def set_cached_jobs(jobs, limit: int, offset: int):
    try:
        redis_client.set(
            get_cache_key(limit, offset),
            json.dumps(jobs, default=str),
            ex=JOBS_CACHE_TTL,
        )
    except RedisError:
        logger.warning("Redis unavailable, skipping jobs cache write")


def delete_cached_jobs():
    try:
        keys = list(redis_client.scan_iter(match=JOBS_PAGE_PATTERN))
        if keys:
            redis_client.delete(*keys)
    except RedisError:
        logger.warning("Redis unavailable, skipping jobs cache invalidation")