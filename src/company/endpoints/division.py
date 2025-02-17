import logging

from fastapi import APIRouter, Depends

from company.repository import DivisionRepository, get_division_repo
from company.schemas import (
    DivisionSchemaCreate,
    DivisionSchemaDB,
    DivisionSchemaUpdate,
)
from company.validatiors import (
    check_equal_id_for_parent_id,
    check_fields_duplicate,
    validate_object_for_id,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[DivisionSchemaDB],
    summary="Получить все отделы",
    description="Получает отделы из базы данных.",
)
async def get_all_division(
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    objs = await division_repo.get_multi()
    return objs


@router.get(
    "/{division_id}/",
    response_model=DivisionSchemaDB,
    summary="Получить отдел по id",
    description="Получает отдел по id из базы данных.",
)
async def get_division(
    division_id: int,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    await validate_object_for_id(division_id, division_repo)
    return await division_repo.get(obj_id=division_id)


@router.post(
    "/",
    response_model=DivisionSchemaDB,
    summary="Создает отдел.",
    status_code=201,
)
async def create_division(
    division: DivisionSchemaCreate,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    await check_fields_duplicate(division, ("name",), division_repo)
    if division.parent_id:
        await validate_object_for_id(division.parent_id, division_repo)
    new_obj = await division_repo.create(obj_in=division)
    return new_obj


@router.delete(
    "/{division_id}/",
    summary="Удалить отдел.",
    status_code=204,
)
async def delete_division(
    division_id: int,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    await validate_object_for_id(division_id, division_repo)
    division = await division_repo.get(obj_id=division_id)
    division = await division_repo.remove(db_obj=division)
    return


@router.patch(
    "/{division_id}/",
    response_model=DivisionSchemaDB,
    summary="Изменить отдел.",
    status_code=201,
)
async def change_division(
    division_id: int,
    obj_in: DivisionSchemaUpdate,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    await validate_object_for_id(division_id, division_repo)
    await check_fields_duplicate(obj_in, ("name",), division_repo)
    division = await division_repo.get(obj_id=division_id)
    if obj_in.parent_id:
        await validate_object_for_id(obj_in.parent_id, division_repo)
    check_equal_id_for_parent_id(division_id, obj_in.parent_id)
    update_obj = await division_repo.update(division, obj_in)
    return update_obj
