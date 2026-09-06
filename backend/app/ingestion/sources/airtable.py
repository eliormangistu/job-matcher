import re
import json
import requests
from pathlib import Path

from app.ingestion.sources.base import JobSource
from app.schemas.airtable import (
    AirtableResponse,
    AirtableRow,
    AirtableColumn,
)
from app.core.logger import logger


class AirtableSource(JobSource):
    def fetch_data(self) -> AirtableResponse:
        logger.info(
            "Airtable data fetch started",
            extra={
                "service": "airtable",
                "action": "fetch_data",
            },
        )

        data_dir = Path(__file__).parents[3] / "data"

        try:
            with open(
                data_dir / "airtable.html",
                encoding="utf-8",
            ) as f:
                html = f.read()

            logger.info(
                "Airtable HTML loaded",
                extra={
                    "service": "airtable",
                    "action": "load_html",
                },
            )

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

            headers_match = re.search(
                r"var headers = (\{.*?\});",
                html,
                re.S,
            )

            if not headers_match:
                logger.error(
                    "Airtable headers not found",
                    extra={
                        "service": "airtable",
                        "action": "extract_headers",
                    },
                )
                raise RuntimeError("Airtable headers not found")

            headers = json.loads(headers_match.group(1))
            headers["x-time-zone"] = "Asia/Jerusalem"

            logger.info(
                "Airtable request started",
                extra={
                    "service": "airtable",
                    "action": "request",
                },
            )

            response = requests.get(
                url,
                headers=headers,
                timeout=(5, 30),
            )

            response.raise_for_status()

            logger.info(
                "Airtable request completed",
                extra={
                    "service": "airtable",
                    "action": "request",
                    "status_code": response.status_code,
                },
            )

            data = AirtableResponse.model_validate(response.json())

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
