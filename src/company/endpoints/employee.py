from fastapi import APIRouter, Depends

import logging

from company.repository import EmployeeRepository, get_employee_repo
from company.schemas import (
    EmployeeSchemaDB,
    EmployeeSchemasCreate,
    EmployeeSchemasUpdate,
)
from company.validatiors import validate_object_for_id

router = APIRouter()


@router.get(
    "/",
    response_model=list[EmployeeSchemaDB],
    summary="Получить всех сотрудников",
    description="Получает сотрудников из базы данных.",
)
async def get_all_employee(
    employee_repo: EmployeeRepository = Depends(get_employee_repo),
):
    objs = await employee_repo.get_multi()
    return objs


@router.get(
    "/{employee_id}/",
    response_model=EmployeeSchemaDB,
    summary="Получить сотрудника по id",
    description="Получает сотрудника по id из базы данных.",
)
async def get_employee(
    employee_id: int,
    employee_repo: EmployeeRepository = Depends(get_employee_repo),
):
    await validate_object_for_id(employee_id, employee_repo)
    return await employee_repo.get(obj_id=employee_id)


@router.post(
    "/",
    response_model=EmployeeSchemaDB,
    summary="Создает сотрудника.",
    status_code=201,
)
async def create_employee(
    employee: EmployeeSchemasCreate,
    employee_repo: EmployeeRepository = Depends(get_employee_repo),
):
    new_project = await employee_repo.create(obj_in=employee)
    return new_project


@router.delete(
    "/{employee_id}/",
    summary="Удалить сотрудника.",
    status_code=204,
)
async def delete_employee(
    employee_id: int,
    employee_repo: EmployeeRepository = Depends(get_employee_repo),
):
    await validate_object_for_id(employee_id, employee_repo)
    employee = await employee_repo.get(obj_id=employee_id)
    await employee_repo.remove(db_obj=employee)
    return


@router.patch(
    "/{employee_id}/",
    response_model=EmployeeSchemaDB,
    summary="Изменить сотрудника.",
    status_code=201,
)
async def change_employee(
    employee_id: int,
    obj_in: EmployeeSchemasUpdate,
    employee_repo: EmployeeRepository = Depends(get_employee_repo),
):
    await validate_object_for_id(employee_id, employee_repo)
    employee = await employee_repo.get(obj_id=employee_id)
    return await employee_repo.update(employee, obj_in)
