from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class StatusBase(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150,
        title="Name",
        description="Наименование статуса сотрудника.",
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "name": "Декрет",
            }
        }

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            exc_msg = "Значение поля name не должно быть пусты."
            raise HTTPException(status_code=422, detail=exc_msg)
        return value


class StatusSchemaCreate(StatusBase):
    pass


class StatusSchemaUpdate(StatusBase):
    name: Optional[str] = Field(
        min_length=1, max_length=150, title="Name", description="Имя отдела"
    )


class StatusSchemaDB(StatusBase):
    id: int = Field(
        title="Id Status in DB", description="Id статуса в базе данных"
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Декрет",
            }
        }
