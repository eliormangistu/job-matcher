from contentful import Client

from app.core.config import SPACE_ID, ACCESS_TOKEN
from app.core.logger import ServiceLogger

logger = ServiceLogger("contentful")

client = Client(
    SPACE_ID,
    ACCESS_TOKEN,
    environment="master",
)


def get_all_content() -> dict:
    logger.info(
        "Fetching content from Contentful",
        action="get_all_content",
    )

    try:
        entries = client.entries(
            {
                "content_type": "jobMatcher",
                "limit": 1,
            }
        )

        if not entries:
            logger.warning(
                "No content found in Contentful",
                action="get_all_content",
            )
            return {}

        entry = entries[0]

        logger.info(
            "Content fetched successfully from Contentful",
            action="get_all_content",
        )

        return entry.fields()

    except Exception:
        logger.exception(
            "Failed to fetch content from Contentful",
            action="get_all_content",
        )
        raise
