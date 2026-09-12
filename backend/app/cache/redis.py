# import redis

# from app.core.config import REDIS_HOST, REDIS_PORT


# redis_client = redis.Redis(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     decode_responses=True
# )

import redis

from app.core.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
