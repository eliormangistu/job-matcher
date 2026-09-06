import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from app.ingestion.sources.airtable import AirtableSource
from app.core.config import JOB_LOOKBACK_DAYS
from app.ingestion.filters import (
    is_allowed_field,
    is_allowed_experience,
)
from app.ingestion.mappers import build_choice_maps, map_single, map_job

OUTPUT_FILE = Path(__file__).parents[2] / "data" / "jobs.json"


def ingest_jobs():
    source = AirtableSource()

    data = source.fetch_data()
    rows = source.fetch_jobs(data)
    columns = source.fetch_columns(data)

    choice_maps = build_choice_maps(columns)

    field_map = choice_maps.get("Field", {})
    location_map = choice_maps.get("Location", {})
    industry_map = choice_maps.get("Company Industry", {})
    language_map = choice_maps.get("Language requirement", {})

    three_months_ago = datetime.now(timezone.utc) - timedelta(days=JOB_LOOKBACK_DAYS)

    for column in columns:
        print(column["id"], "=>", column["name"])

    jobs = []

    for row in rows:
        values = row.get("cellValuesByColumnId", {})

        posted_value = values.get("fldQP1mEhbNlwJMA1")

        if not posted_value:
            continue

        try:
            posted_date = datetime.fromisoformat(posted_value.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            continue

        if posted_date < three_months_ago:
            continue

        field = map_single(values.get("fldHy6G67uu7RvU7W"), field_map)

        if not is_allowed_field(field):
            continue

        min_experience = values.get("fldfuYXHAHe1DsL8X")

        if not is_allowed_experience(min_experience):
            continue

        job = map_job(
            row,
            values,
            field,
            industry_map,
            location_map,
            language_map,
            posted_value,
            min_experience,
        )

    jobs.append(job)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    return jobs


if __name__ == "__main__":
    jobs = ingest_jobs()

    print(f"Exported {len(jobs)} jobs")
    print(f"Saved to {OUTPUT_FILE}")

    if jobs:
        print("\nFirst job:")
        print(json.dumps(jobs[0], ensure_ascii=False, indent=2))
