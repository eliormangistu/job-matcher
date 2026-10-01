from pydantic import BaseModel
from typing import Any


class AirtableRow(BaseModel):
    id: str
    createdTime: str
    cellValuesByColumnId: dict[str, Any]


class AirtableColumn(BaseModel):
    id: str
    name: str
    description: str | None = None
    type: str
    typeOptions: dict[str, Any] | None = None


class AirtableTable(BaseModel):
    rows: list[AirtableRow]
    columns: list[AirtableColumn]


class AirtableData(BaseModel):
    table: AirtableTable


class AirtableResponse(BaseModel):
    data: AirtableData
