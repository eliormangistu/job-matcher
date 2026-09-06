def build_choice_maps(columns):
    choice_maps = {}

    for column in columns:
        column_name = column["name"]
        type_options = column.get("typeOptions") or {}
        choices = type_options.get("choices", {})

        if choices:
            choice_maps[column_name] = {
                choice_id: choice["name"] for choice_id, choice in choices.items()
            }

    return choice_maps


def map_single(value, mapping):
    if value is None:
        return None

    return mapping.get(value, value)


def map_job(
    row,
    values,
    field,
    industry_map,
    location_map,
    language_map,
    posted_value,
    min_experience,
):
    return {
        "airtable_id": row.get("id"),
        "job_id": values.get("fldiWYpIMh67vZGjh"),
        "created_time": row.get("createdTime"),
        "discovered": values.get("fld0IWlQzimjOyKcm"),
        "field": field,
        "title": values.get("fldPX7uQTBeLM8qIM"),
        "company": values.get("fldLutadLsnGiv7oZ"),
        "company_industry": _map_multiple(
            values.get("fld9UFlS0Yxfo1AuX", []), industry_map
        ),
        "position_link": values.get("fldDhjjRS8LR94g9q"),
        "scope": values.get("fldcK55EmF5hONqxu"),
        "location": _map_multiple(values.get("fldKjkUS3dypwOv9e", []), location_map),
        "min_experience": min_experience,
        "job_description": values.get("fldwOL044G6IGcDKj"),
        "requirements": values.get("fldIuBO23JewsToWa"),
        "language_requirement": _map_multiple(
            values.get("fld669xsm4GH6eOHc", []), language_map
        ),
        "education_requirements": values.get("fldfEcfdf2i8poBck"),
        "posted": posted_value,
    }


def _map_multiple(values, mapping):
    if not values:
        return []

    return [mapping.get(value, value) for value in values]
