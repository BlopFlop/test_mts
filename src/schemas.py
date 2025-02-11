from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "message": "Confirm operations.",
            }
        }


class CreateSchemaType(BaseModel):
    """Type schema."""

    class Config:
        json_schema_extra = {
            "example": {
                "any": "type schema",
            }
        }


class UpdateSchemaType(CreateSchemaType):
    """Create schema for Seciton."""


class DBSchemaType(CreateSchemaType):
    """Create schema for Seciton."""

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "any": "test schema",
            }
        }
