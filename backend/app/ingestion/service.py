import json
from datetime import datetime, timedelta, timezone

from app.ingestion.sources.airtable import AirtableSource
from app.core.config import ALLOWED_JOB_FIELDS, JOB_LOOKBACK_DAYS, MAX_JOB_EXPERIENCE

OUTPUT_FILE = "jobs.json"

ALLOWED_FIELDS = ALLOWED_JOB_FIELDS


def build_choice_maps(columns):
    choice_maps = {}

    for column in columns:
        column_name = column["name"]
        type_options = column.get("typeOptions") or {}
        choices = type_options.get("choices", {})

        if choices:
            choice_maps[column_name] = {
                choice_id: choice["name"]
                for choice_id, choice in choices.items()
            }

    return choice_maps


def map_single(value, mapping):
    if value is None:
        return None

    return mapping.get(value, value)


def map_multiple(values, mapping):
    if not values:
        return []

    return [mapping.get(value, value) for value in values]


def ingest_jobs():
    source = AirtableSource()

    rows = source.fetch_jobs()
    columns = source.fetch_columns()

    choice_maps = build_choice_maps(columns)

    field_map = choice_maps.get("Field", {})
    location_map = choice_maps.get("Location", {})
    industry_map = choice_maps.get("Company Industry", {})
    language_map = choice_maps.get("Language requirement", {})

    three_months_ago = (
        datetime.now(timezone.utc) - timedelta(days=JOB_LOOKBACK_DAYS)
    )

    print("ROWS:", len(rows))
    print("COLUMNS:")

    for column in columns:
     print(column["id"], "=>", column["name"])
  
    jobs = []

    for row in rows:
        values = row.get("cellValuesByColumnId", {})

        posted_value = values.get("fldQP1mEhbNlwJMA1")

        if not posted_value:
            continue

        try:
            posted_date = datetime.fromisoformat(
                posted_value.replace("Z", "+00:00")
            )
        except (ValueError, TypeError):
            continue

        if posted_date < three_months_ago:
            continue

        field = map_single(
            values.get("fldHy6G67uu7RvU7W"),
            field_map
        )

        if field not in ALLOWED_FIELDS:
            continue

        min_experience = values.get(
            "fldfuYXHAHe1DsL8X"
        )

        if min_experience is not None:
            try:
                if int(min_experience) > MAX_JOB_EXPERIENCE:
                    continue
            except (ValueError, TypeError):
                pass

        job = {
            "airtable_id": row.get("id"),
            "job_id": values.get("fldiWYpIMh67vZGjh"),
            "created_time": row.get("createdTime"),
            "discovered": values.get(
                "fld0IWlQzimjOyKcm"
            ),
            "field": field,
            "title": values.get(
                "fldPX7uQTBeLM8qIM"
            ),
            "company": values.get(
                "fldLutadLsnGiv7oZ"
            ),
            "company_industry": map_multiple(
                values.get(
                    "fld9UFlS0Yxfo1AuX",
                    []
                ),
                industry_map
            ),
            "position_link": values.get(
                "fldDhjjRS8LR94g9q"
            ),
            "scope": values.get(
                "fldcK55EmF5hONqxu"
            ),
            "location": map_multiple(
                values.get(
                    "fldKjkUS3dypwOv9e",
                    []
                ),
                location_map
            ),
            "min_experience": min_experience,
            "job_description": values.get(
                "fldwOL044G6IGcDKj"
            ),
            "requirements": values.get(
                "fldIuBO23JewsToWa"
            ),
            "language_requirement": map_multiple(
                values.get(
                    "fld669xsm4GH6eOHc",
                    []
                ),
                language_map
            ),
            "education_requirements": values.get(
                "fldfEcfdf2i8poBck"
            ),
            "salary": values.get(
                "fld2iXGjCqY0y2jbT"
            ),
            "point_of_contact": values.get(
                "fldGIE6tCNlj6MQwD"
            ),
            "linkedin": values.get(
                "fldELqhH0PkwXqdod"
            ),
            "email": values.get(
                "fldCEYOJHJndLti9m"
            ),
            "phone": values.get(
                "fldIXyeUs16eNxkBY"
            ),
            "posted": posted_value,
            "job_id": values.get(
                "fldiWYpIMh67vZGjh"
            ),
        }

        jobs.append(job)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            jobs,
            f,
            ensure_ascii=False,
            indent=2
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
                indent=2
            )
        )