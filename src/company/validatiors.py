from http import HTTPStatus
from typing import Sequence

from fastapi import HTTPException

from repository import RepositoryBase
from schemas import CreateSchemaType, DBSchemaType, UpdateSchemaType


async def check_fields_duplicate(
    schema: CreateSchemaType | UpdateSchemaType,
    fields_set: Sequence[str],
    repository: RepositoryBase,
) -> None | HTTPException:
    """Check duplicate unique field in DB."""
    elements: list[DBSchemaType] = await repository.get_multi()

    ununique_fields = {}
    for element in elements:
        for field in fields_set:
            schema_attr = getattr(schema, field)
            element_attr = getattr(element, field)
            if schema_attr and schema_attr == element_attr:
                ununique_fields[field] = schema_attr
        if ununique_fields:
            ununique_fields = ", ".join(
                [f"{key} = {value}" for key, value in ununique_fields.items()]
            )
            exc_msg = (
                "Вы должны передать уникальные значения,"
                f" значения полей уже существуют: {ununique_fields} "
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=exc_msg,
            )


async def validate_object_for_id(obj_id: int, repository: RepositoryBase):
    obj_db = await repository.get(obj_id=obj_id)
    if not obj_db:
        exc_msg = f"Объекта под id {obj_id} не существует в базе данных."
        raise HTTPException(status_code=400, detail=exc_msg)
    return obj_db
