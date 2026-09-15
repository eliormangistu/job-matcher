import re
import requests

from app.ingestion.sources.base import JobSource
from app.schemas.airtable import (
    AirtableResponse,
    AirtableRow,
    AirtableColumn,
)
from app.core.logger import logger
from app.core.config import AIRTABLE_VIEW_URL


class AirtableSource(JobSource):
    def fetch_data(self) -> AirtableResponse:
        logger.info(
            "Airtable data fetch started",
            extra={
                "service": "airtable",
                "action": "fetch_data",
            },
        )

        try:
            # Load the public Airtable Shared View
            session = requests.Session()

            browser_headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                ),
            }

            response = session.get(
                AIRTABLE_VIEW_URL,
                headers=browser_headers,
                timeout=(5, 30),
            )

            response.raise_for_status()
            html = response.text

            logger.info(
                "Airtable Shared View loaded",
                extra={
                    "service": "airtable",
                    "action": "load_shared_view",
                    "status_code": response.status_code,
                },
            )

            # Extract the internal Airtable data URL
            url_match = re.search(
                r'urlWithParams:\s*"([^"]+)"',
                html,
            )

            if not url_match:
                logger.error(
                    "Airtable URL not found",
                    extra={
                        "service": "airtable",
                        "action": "extract_url",
                    },
                )
                raise RuntimeError("Airtable URL not found")

            url = url_match.group(1)
            url = url.replace(r"\u002F", "/")
            url = url.replace(r"\u0026", "&")
            url = "https://airtable.com" + url

            # Headers used by Airtable's Shared View request
            headers = {
                "x-early-prefetch": "true",
                "x-user-locale": "en",
                "x-airtable-application-id": ("appwewqLk7iUY4azc"),
                "X-Requested-With": "XMLHttpRequest",
                "x-airtable-inter-service-client": "webClient",
                "x-airtable-accept-msgpack": "true",
                "x-time-zone": "Asia/Jerusalem",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36"
                ),
                "Accept": ("application/json, text/plain, */*"),
                "Referer": AIRTABLE_VIEW_URL,
            }

            logger.info(
                "Airtable data request started",
                extra={
                    "service": "airtable",
                    "action": "request",
                },
            )

            data_response = session.get(
                url,
                headers=headers,
                timeout=(5, 30),
            )

            data_response.raise_for_status()

            logger.info(
                "Airtable data request completed",
                extra={
                    "service": "airtable",
                    "action": "request",
                    "status_code": data_response.status_code,
                },
            )

            data = AirtableResponse.model_validate(data_response.json())

            logger.info(
                "Airtable response parsed",
                extra={
                    "service": "airtable",
                    "action": "parse_response",
                },
            )

            return data

        except Exception:
            logger.exception(
                "Airtable data fetch failed",
                extra={
                    "service": "airtable",
                    "action": "fetch_data",
                },
            )
            raise

    def fetch_jobs(
        self,
        data: AirtableResponse,
    ) -> list[AirtableRow]:
        jobs = data.data.table.rows

        logger.info(
            "Airtable jobs extracted",
            extra={
                "service": "airtable",
                "action": "fetch_jobs",
                "count": len(jobs),
            },
        )

        return jobs

    def fetch_columns(
        self,
        data: AirtableResponse,
    ) -> list[AirtableColumn]:
        columns = data.data.table.columns

        logger.info(
            "Airtable columns extracted",
            extra={
                "service": "airtable",
                "action": "fetch_columns",
                "count": len(columns),
            },
        )

        return columns
