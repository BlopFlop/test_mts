from typing import Optional

from fastapi import HTTPException
from pydantic import (
    BaseModel, Field, PositiveInt, field_validator, model_validator
)


class DivisionBase(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150,
        title="Name",
        description="Имя отдела"
    )
    parent_id: Optional[PositiveInt] = Field(
        None,
        title="Parent id",
        description="Родительский отдел."
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "name": "Отдел контроля строительства",
                "parent_id": 1,
            }
        }

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            exc_msg = "Значение поля name не должно быть пусты."
            raise HTTPException(status_code=422, detail=exc_msg)
        return value


class DivisionSchemaCreate(DivisionBase):
    pass


class DivisionSchemaUpdate(DivisionBase):
    name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Name",
        description="Имя отдела"
    )


class DivisionSchemaDB(DivisionBase):
    id: int = Field(
        title="Id Division in DB",
        description="Id Отдела в базе данных"
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Отдел контроля строительства",
            }
        }
