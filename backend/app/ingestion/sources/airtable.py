import re
import json
import requests
from pathlib import Path

from app.ingestion.sources.base import JobSource


class AirtableSource(JobSource):
    def fetch_data(self) -> dict:
        data_dir = Path(__file__).parents[3] / "data"

        with open(data_dir / "airtable.html", encoding="utf-8") as f:
            html = f.read()

        url_match = re.search(r'urlWithParams:\s*"([^"]+)"', html)

        if not url_match:
            raise RuntimeError("Airtable URL not found")

        url = url_match.group(1)
        url = url.replace(r"\u002F", "/")
        url = url.replace(r"\u0026", "&")
        url = "https://airtable.com" + url

        headers_match = re.search(r"var headers = (\{.*?\});", html, re.S)

        if not headers_match:
            raise RuntimeError("Airtable headers not found")

        headers = json.loads(headers_match.group(1))
        headers["x-time-zone"] = "Asia/Jerusalem"

        response = requests.get(
            url,
            headers=headers,
            timeout=(5, 30),
        )
        response.raise_for_status()

        return response.json()

    def fetch_jobs(self, data: dict) -> list[dict]:
        return data["data"]["table"]["rows"]

    def fetch_columns(self, data: dict) -> list[dict]:
        return data["data"]["table"]["columns"]
