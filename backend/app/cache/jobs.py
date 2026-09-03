import json

from app.cache.redis import redis_client
from app.core.config import JOBS_CACHE_TTL

JOBS_CACHE_KEY = "jobs:all"


def get_cached_jobs():
    cached_jobs = redis_client.get(JOBS_CACHE_KEY)

    if cached_jobs is None:
        return None

    return json.loads(cached_jobs)


def set_cached_jobs(jobs):
    redis_client.set(
        JOBS_CACHE_KEY,
        json.dumps(jobs),
        ex=JOBS_CACHE_TTL
    )


def delete_cached_jobs():
    redis_client.delete(JOBS_CACHE_KEY)