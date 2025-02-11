from fastapi import APIRouter, Depends

from company.repository import PositionRepository, get_position_repo
from company.schemas import (
    PositionSchemaCreate,
    PositionSchemaUpdate,
    PositionSchemaDB
)
from company.validatiors import validate_object_for_id, check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[PositionSchemaDB],
    summary="Получить все должности",
    description="Получает должности из базы данных.",
)
async def get_all_positions(
    position_repo: PositionRepository = Depends(get_position_repo),
):
    return await position_repo.get_multi()


@router.get(
    "/{position_id}/",
    response_model=PositionSchemaDB,
    summary="Получить должность по id",
    description="Получает должность по id из базы данных.",
)
async def get_position(
    position_id: int,
    position_repo: PositionRepository = Depends(get_position_repo),
):
    await validate_object_for_id(position_id, position_repo)
    return await position_repo.get(obj_id=position_id)


@router.post(
    "/",
    response_model=PositionSchemaDB,
    summary="Создает должность.",
    status_code=201,
)
async def create_position(
    position: PositionSchemaCreate,
    position_repo: PositionRepository = Depends(get_position_repo),
):
    await check_fields_duplicate(position, ("name",), position_repo)
    new_position = await position_repo.create(obj_in=position)
    return new_position


@router.delete(
    "/{position_id}/",
    summary="Удалить должность.",
    status_code=204,
)
async def delete_position(
    position_id: int,
    position_repo: PositionRepository = Depends(get_position_repo),
):
    await validate_object_for_id(position_id, position_repo)
    position = await position_repo.get(obj_id=position_id)
    await position_repo.remove(db_obj=position)
    return


@router.patch(
    "/{position_id}/",
    response_model=PositionSchemaDB,
    summary="Изменить должность.",
    status_code=201,
)
async def change_position(
    position_id: int,
    obj_in: PositionSchemaUpdate,
    position_repo: PositionRepository = Depends(get_position_repo),
):
    await check_fields_duplicate(obj_in, ("name",), position_repo)
    await validate_object_for_id(position_id, position_repo)
    position = await position_repo.get(obj_id=position_id)
    return await position_repo.update(position, obj_in)
