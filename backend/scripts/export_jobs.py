import json
from datetime import datetime, timedelta

INPUT_FILE = "airtable_data.json"
OUTPUT_FILE = "jobs.json"


with open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)


table = data["data"]["table"]
rows = table["rows"]
columns = table["columns"]


# Build Airtable ID -> human-readable name mappings
choice_maps = {}
three_months_ago = datetime.now() - timedelta(days=90)

for column in columns:
    column_name = column["name"]
    type_options = column.get("typeOptions") or {}
    choices = type_options.get("choices", {})

    if choices:
        choice_maps[column_name] = {
            choice_id: choice["name"] for choice_id, choice in choices.items()
        }


FIELD_MAP = choice_maps.get("Field", {})
LOCATION_MAP = choice_maps.get("Location", {})
INDUSTRY_MAP = choice_maps.get("Company Industry", {})

ALLOWED_FIELDS = {
    "Software Engineering",
    "Data Science, ML & Algorithms",
    "DevOps",
    "Data Engineering",
    "Frontend Development",
    "Mobile Development",
    "Embedded, Low Level & Firmware Engineering",
}


def map_single(value, mapping):
    if value is None:
        return None

    return mapping.get(value, value)


def map_multiple(values, mapping):
    if not values:
        return []

    return [mapping.get(value, value) for value in values]


jobs = []

for row in rows:
    values = row.get("cellValuesByColumnId", {})

    # Filter by posted date: last 90 days
    posted_value = values.get("fldQP1mEhbNlwJMA1")

    if not posted_value:
        continue

    try:
        posted_date = datetime.fromisoformat(
            posted_value.replace("Z", "+00:00")
        ).replace(tzinfo=None)
    except (ValueError, TypeError):
        continue

    if posted_date < three_months_ago:
        continue

    field = map_single(values.get("fldHy6G67uu7RvU7W"), FIELD_MAP)

    if field not in ALLOWED_FIELDS:
        continue

    min_experience = values.get("fldfuYXHAHe1DsL8X")

    if min_experience is not None:
        try:
            if int(min_experience) > 5:
                continue
        except (ValueError, TypeError):
            pass

    job = {
        "id": row.get("id"),
        "job_id": values.get("fldiWYpIMh67vZGjh"),
        "created_time": row.get("createdTime"),
        "discovered": values.get("fld0IWlQzimjOyKcm"),
        "field": field,
        "title": values.get("fldPX7uQTBeLM8qIM"),
        "company": values.get("fldLutadLsnGiv7oZ"),
        "company_industry": map_multiple(
            values.get("fld9UFlS0Yxfo1AuX", []), INDUSTRY_MAP
        ),
        "position_link": values.get("fldDhjjRS8LR94g9q"),
        "scope": values.get("fldcK55EmF5hONqxu"),
        "location": map_multiple(values.get("fldKjkUS3dypwOv9e", []), LOCATION_MAP),
        "min_experience": values.get("fldfuYXHAHe1DsL8X"),
        "job_description": values.get("fldwOL044G6IGcDKj"),
        "requirements": values.get("fldIuBO23JewsToWa"),
        "language_requirement": map_multiple(
            values.get("fld669xsm4GH6eOHc", []),
            choice_maps.get("Language requirement", {}),
        ),
        "education_requirements": values.get("fldfEcfdf2i8poBck"),
        "posted": posted_value,
    }

    jobs.append(job)


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)


print(f"Exported {len(jobs)} jobs")
print(f"Saved to {OUTPUT_FILE}")

print("\nFirst job:")
print(json.dumps(jobs[0], ensure_ascii=False, indent=2))
