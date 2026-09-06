from typing import Any

from app.schemas.airtable import AirtableRow, AirtableColumn
from app.ingestion.fields import AirtableField
from app.core.logger import logger


def build_choice_maps(columns: list[AirtableColumn]):
    logger.info(
        "Building Airtable choice maps",
        extra={
            "service": "mappers",
            "action": "build_choice_maps",
            "columns_count": len(columns),
        },
    )

    choice_maps = {}

    for column in columns:
        column_name = column.name
        type_options = column.typeOptions or {}
        choices = type_options.get("choices", {})

        if choices:
            choice_maps[column_name] = {
                choice_id: choice["name"] for choice_id, choice in choices.items()
            }

    logger.info(
        "Airtable choice maps built",
        extra={
            "service": "mappers",
            "action": "build_choice_maps",
            "maps_count": len(choice_maps),
        },
    )

    return choice_maps


def map_single(value, mapping):
    if value is None:
        return None

    return mapping.get(value, value)


def map_job(
    row: AirtableRow,
    values: dict[str, Any],
    field,
    industry_map,
    location_map,
    language_map,
    scope_map,
    posted_value,
    min_experience,
):
    return {
        "airtable_id": row.id,
        "job_id": values.get(AirtableField.JOB_ID),
        "created_time": row.createdTime,
        "discovered": values.get(AirtableField.DISCOVERED),
        "field": field,
        "title": values.get(AirtableField.JOB_TITLE),
        "company": values.get(AirtableField.COMPANY),
        "company_industry": _map_multiple(
            values.get(AirtableField.COMPANY_INDUSTRY, []),
            industry_map,
        ),
        "position_link": values.get(AirtableField.POSITION_LINK),
        "scope": map_single(
            values.get(AirtableField.SCOPE),
            scope_map,
        ),
        "location": _map_multiple(
            values.get(AirtableField.LOCATION, []),
            location_map,
        ),
        "min_experience": min_experience,
        "job_description": values.get(AirtableField.JOB_DESCRIPTION),
        "requirements": values.get(AirtableField.REQUIREMENTS),
        "language_requirement": _map_multiple(
            values.get(AirtableField.LANGUAGE_REQUIREMENT, []),
            language_map,
        ),
        "education_requirements": values.get(AirtableField.EDUCATION_REQUIREMENTS),
        "posted": posted_value,
    }


def _map_multiple(values, mapping):
    if not values:
        return []

    return [mapping.get(value, value) for value in values]
