from typing import Optional

from pydantic import BaseModel, Field


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
