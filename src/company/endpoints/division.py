from fastapi import APIRouter, Depends

from company.repository import DivisionRepository, get_division_repo
from company.schemas import (
    DivisionSchemaCreate,
    DivisionSchemaUpdate,
    DivisionSchemaDB
)
from company.validatiors import validate_object_for_id

router = APIRouter()


@router.get(
    "/",
    response_model=list[DivisionSchemaDB],
    summary="Получить всех сотрудников",
    description="Получает сотрудников из базы данных.",
)
async def get_all_division(
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    return await division_repo.get_multi()


@router.get(
    "/{division_id}/",
    response_model=DivisionSchemaDB,
    summary="Получить сотрудника по id",
    description="Получает сотрудника по id из базы данных.",
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
    summary="Создает сотрудника.",
    division_code=201,
)
async def create_division(
    division: DivisionSchemaCreate,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    new_project = await division_repo.create(obj_in=division)
    return new_project


@router.delete(
    "/{division_id}/",
    summary="Удалить сотрудника.",
    division_code=204,
)
async def delete_division(
    division_id: int,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    await validate_object_for_id(division_id, division_repo)
    division = await division_repo.get(obj_id=division_id)
    await division_repo.remove(db_obj=division)
    return


@router.patch(
    "/{division_id}/",
    response_model=DivisionSchemaDB,
    summary="Изменить сотрудника.",
    division_code=201,
)
async def change_division(
    division_id: int,
    obj_in: DivisionSchemaUpdate,
    division_repo: DivisionRepository = Depends(get_division_repo),
):
    await validate_object_for_id(division_id, division_repo)
    division = await division_repo.get(obj_id=division_id)
    return await division_repo.update(division, obj_in)
