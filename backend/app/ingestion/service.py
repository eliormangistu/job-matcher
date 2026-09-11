import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from app.ingestion.sources.airtable import AirtableSource
from app.core.config import JOB_LOOKBACK_DAYS
from app.core.logger import logger
from app.ingestion.filters import (
    is_allowed_field,
    is_allowed_experience,
)
from app.ingestion.mappers import build_choice_maps, map_single, map_job
from app.ingestion.fields import AirtableField


OUTPUT_FILE = Path(__file__).parents[2] / "data" / "jobs.json"


def ingest_jobs():
    logger.info(
        "Job ingestion started",
        extra={
            "service": "ingestion",
            "action": "ingest_jobs",
            "lookback_days": JOB_LOOKBACK_DAYS,
        },
    )

    source = AirtableSource()
    data = source.fetch_data()

    rows = source.fetch_jobs(data)
    columns = source.fetch_columns(data)

    logger.info(
        "Airtable data loaded",
        extra={
            "service": "ingestion",
            "action": "load_data",
            "rows_count": len(rows),
            "columns_count": len(columns),
        },
    )

    choice_maps = build_choice_maps(columns)

    field_map = choice_maps.get("Field", {})
    location_map = choice_maps.get("Location", {})
    industry_map = choice_maps.get("Company Industry", {})
    language_map = choice_maps.get("Language requirement", {})
    scope_map = choice_maps.get("Scope", {})

    lookback_date = datetime.now(timezone.utc) - timedelta(days=JOB_LOOKBACK_DAYS)

    jobs = []

    skipped_no_posted = 0
    skipped_invalid_date = 0
    skipped_old = 0
    skipped_field = 0
    skipped_experience = 0

    for row in rows:
        values = row.cellValuesByColumnId
        posted_value = values.get(AirtableField.POSTED)

        if not posted_value:
            skipped_no_posted += 1
            continue

        try:
            posted_date = datetime.fromisoformat(posted_value.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            skipped_invalid_date += 1
            continue

        if posted_date < lookback_date:
            skipped_old += 1
            continue

        field = map_single(
            values.get(AirtableField.FIELD),
            field_map,
        )

        if not is_allowed_field(field):
            skipped_field += 1
            continue

        min_experience = values.get(AirtableField.MIN_EXPERIENCE)

        if not is_allowed_experience(min_experience):
            skipped_experience += 1
            continue

        job = map_job(
            row,
            values,
            field,
            industry_map,
            location_map,
            language_map,
            scope_map,
            posted_value,
            min_experience,
        )

        jobs.append(job)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            jobs,
            f,
            ensure_ascii=False,
            indent=2,
        )

    logger.info(
        "Job ingestion completed",
        extra={
            "service": "ingestion",
            "action": "ingest_jobs",
            "input_rows": len(rows),
            "exported_jobs": len(jobs),
            "skipped_no_posted": skipped_no_posted,
            "skipped_invalid_date": skipped_invalid_date,
            "skipped_old": skipped_old,
            "skipped_field": skipped_field,
            "skipped_experience": skipped_experience,
            "output_file": str(OUTPUT_FILE),
        },
    )

    return jobs


if __name__ == "__main__":
    jobs = ingest_jobs()

    print(f"Exported {len(jobs)} jobs")
    print(f"Saved to {OUTPUT_FILE}")

    if jobs:
        print("\nFirst job:")
        print(
            json.dumps(
                jobs[0],
                ensure_ascii=False,
                indent=2,
            )
        )
