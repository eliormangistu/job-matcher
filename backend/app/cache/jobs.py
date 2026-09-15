import json

from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import JOBS_CACHE_TTL
from app.core.logger import ServiceLogger


logger = ServiceLogger("cache")

JOBS_PAGE_PATTERN = "jobs:page:*"


def get_cache_key(limit: int, offset: int) -> str:
    return f"jobs:page:{offset}:{limit}"


def get_cached_jobs(limit: int, offset: int):
    key = get_cache_key(limit, offset)

    try:
        cached_jobs = redis_client.get(key)

    except RedisError:
        logger.warning(
            "Redis unavailable, skipping jobs cache read",
            action="get_cached_jobs",
            cache_key=key,
        )
        return None

    if cached_jobs is None:
        logger.info(
            "Jobs cache miss",
            action="get_cached_jobs",
            limit=limit,
            offset=offset,
        )
        return None

    jobs = json.loads(cached_jobs)

    logger.info(
        "Jobs cache hit",
        action="get_cached_jobs",
        limit=limit,
        offset=offset,
        count=len(jobs),
    )

    return jobs


def set_cached_jobs(jobs, limit: int, offset: int):
    try:
        redis_client.set(
            get_cache_key(limit, offset),
            json.dumps(jobs, default=str),
            ex=JOBS_CACHE_TTL,
        )

    except RedisError:
        logger.warning(
            "Redis unavailable, skipping jobs cache write",
            action="set_cached_jobs",
        )


def delete_cached_jobs():
    try:
        keys = list(redis_client.scan_iter(match=JOBS_PAGE_PATTERN))

        if keys:
            redis_client.delete(*keys)

        logger.info(
            "Jobs cache invalidated",
            action="delete_cached_jobs",
            deleted_keys=len(keys),
        )

    except RedisError:
        logger.warning(
            "Redis unavailable, skipping jobs cache invalidation",
            action="delete_cached_jobs",
        )
