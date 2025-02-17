from fastapi import APIRouter, Depends

from company.repository import StatusRepository, get_status_repo
from company.schemas import (
    StatusSchemaCreate,
    StatusSchemaDB,
    StatusSchemaUpdate,
)
from company.validatiors import check_fields_duplicate, validate_object_for_id

router = APIRouter()


@router.get(
    "/",
    response_model=list[StatusSchemaDB],
    summary="Получить все статусы",
    description="Получает статусы из базы данных.",
)
async def get_all_status(
    status_repo: StatusRepository = Depends(get_status_repo),
):
    return await status_repo.get_multi()


@router.get(
    "/{status_id}/",
    response_model=StatusSchemaDB,
    summary="Получить статус по id",
    description="Получает статус по id из базы данных.",
)
async def get_status(
    status_id: int,
    status_repo: StatusRepository = Depends(get_status_repo),
):
    await validate_object_for_id(status_id, status_repo)
    return await status_repo.get(obj_id=status_id)


@router.post(
    "/",
    response_model=StatusSchemaDB,
    summary="Создает статус.",
    status_code=201,
)
async def create_status(
    status: StatusSchemaCreate,
    status_repo: StatusRepository = Depends(get_status_repo),
):
    await check_fields_duplicate(status, ("name",), status_repo)
    new_project = await status_repo.create(obj_in=status)
    return new_project


@router.delete(
    "/{status_id}/",
    summary="Удалить статус.",
    status_code=204,
)
async def delete_status(
    status_id: int,
    status_repo: StatusRepository = Depends(get_status_repo),
):
    await validate_object_for_id(status_id, status_repo)
    status = await status_repo.get(obj_id=status_id)
    await status_repo.remove(db_obj=status)
    return


@router.patch(
    "/{status_id}/",
    response_model=StatusSchemaDB,
    summary="Изменить статус.",
    status_code=201,
)
async def change_status(
    status_id: int,
    obj_in: StatusSchemaUpdate,
    status_repo: StatusRepository = Depends(get_status_repo),
):
    check_fields_duplicate(obj_in, ("name",), status_repo)
    await validate_object_for_id(status_id, status_repo)
    status = await status_repo.get(obj_id=status_id)
    return await status_repo.update(status, obj_in)
