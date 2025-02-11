from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


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
            }
        }


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
