from fastapi import HTTPException
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PositionBase(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150,
        title="Name",
        description="Имя должности"
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "name": "менеджер проекта",
            }
        }

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            exc_msg = "Значение поля name не должно быть пусты."
            raise HTTPException(status_code=422, detail=exc_msg)
        return value


class PositionSchemaCreate(PositionBase):
    pass


class PositionSchemaUpdate(PositionBase):
    name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Name",
        description="Имя отдела"
    )


class PositionSchemaDB(PositionBase):
    id: int = Field(
        title="Id Position in DB",
        description="Id Отдела в базе данных"
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "менеджер проекта",
            }
        }
