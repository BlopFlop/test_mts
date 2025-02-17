from datetime import date, datetime, timedelta
from pathlib import Path

from pyxlsb import open_workbook as open_xlsb
from sqlalchemy.orm import Session

from company.repository import (
    DivisionRepository,
    EmployeeRepository,
    PositionRepository,
    StatusRepository,
    get_division_repo,
    get_employee_repo,
    get_position_repo,
    get_status_repo,
)
from company.schemas import (
    DivisionSchemaCreate,
    EmployeeSchemaDB,
    EmployeeSchemasCreate,
    PositionSchemaCreate,
    StatusSchemaCreate,
)
from database import AsyncSessionLocal
from loader.constants import (
    IS_STAFF_EMPLOYEE,
    KEY_DATE_ADD_WORK,
    KEY_DATE_REMOWE_WORK,
    KEY_DEPARTMENT,
    KEY_DIVISION,
    KEY_FULL_NAME,
    KEY_MANAGER,
    KEY_POSITION,
    KEY_SALARY,
    KEY_STAFF,
    KEY_STATUS,
)


def load_data_from_excel_file(
    path_file: Path, sheet_name: str
) -> dict[str, list[str]]:
    with open_xlsb(path_file) as wb:
        with wb.get_sheet(sheet_name) as sheet:
            rows = list(sheet.rows())
            cols = [col.v for col in rows[0]]
            data_to_collumns = {col: [] for col in cols}

            for row in rows[1:]:
                for i, value in enumerate(row):
                    data_to_collumns[cols[i]].append(value.v)

    return data_to_collumns


async def load_status(session: Session, status_name: str) -> None:
    repo: StatusRepository = await get_status_repo(session)

    obj_bd = await repo.get_obj_for_field_arg("name", status_name, False)
    if not obj_bd:
        await repo.create(StatusSchemaCreate(name=status_name))


async def load_division(
    session: Session, division_name: str, department_name: str = None
):
    repo: DivisionRepository = await get_division_repo(session)

    if department_name:
        department_obj = await repo.get_obj_for_field_arg(
            "name", department_name, many=False
        )
        create_schema = DivisionSchemaCreate(
            name=division_name, parent_id=department_obj.id
        )
    else:
        create_schema = DivisionSchemaCreate(name=division_name)

    obj_bd = await repo.get_obj_for_field_arg("name", division_name, False)
    if not obj_bd:
        await repo.create(create_schema)


async def load_position(session: Session, position_name: str) -> None:
    repo: PositionRepository = await get_position_repo(session)
    obj_bd = await repo.get_obj_for_field_arg("name", position_name, False)
    if not obj_bd:
        await repo.create(PositionSchemaCreate(name=position_name))


async def load_employee(
    session: Session, data: dict[str, str], manager_id: int = None
) -> EmployeeSchemaDB:
    division_repo: DivisionRepository = await get_division_repo(session)
    status_repo: StatusRepository = await get_status_repo(session)
    position_repo: PositionRepository = await get_position_repo(session)
    employe_repo: EmployeeRepository = await get_employee_repo(session)

    first_name, last_name, middle_name = data.get(KEY_FULL_NAME).split()

    create_data = {
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
    }
    date_add = data.get(KEY_DATE_ADD_WORK)
    if date_add:
        if isinstance(date_add, str):
            create_data["hire_date"] = datetime.strptime(
                date_add, "%d.%m.%Y"
            ).date()
        else:
            create_data["hire_date"] = date(1900, 1, 1) + timedelta(date_add)

    date_remove = data.get(KEY_DATE_REMOWE_WORK)
    if date_remove:
        if isinstance(date_remove, str):
            create_data["termination_date"] = datetime.strptime(
                date_remove, "%d.%m.%Y"
            ).date()
        else:
            create_data["termination_date"] = date(1900, 1, 1) + timedelta(
                date_remove
            )

    depatment = data.get(KEY_DEPARTMENT)
    division = data.get(KEY_DIVISION)

    if not division:
        depatment_obj = await division_repo.get_obj_for_field_arg(
            "name", depatment, False
        )
        create_data["division_id"] = depatment_obj.id
    else:
        division_obj = await division_repo.get_obj_for_field_arg(
            "name", division, False
        )
        create_data["division_id"] = division_obj.id

    if manager_id:
        create_data["manager_id"] = manager_id

    position = data.get(KEY_POSITION)
    position_obj = await position_repo.get_obj_for_field_arg(
        "name", position, False
    )
    create_data["position_id"] = position_obj.id

    status = data.get(KEY_STATUS)
    status_obj = await status_repo.get_obj_for_field_arg("name", status, False)
    create_data["status_id"] = status_obj.id

    staff = data.get(KEY_STAFF)
    create_data["is_staff"] = True if staff == IS_STAFF_EMPLOYEE else False
    create_data["salary"] = int(data.get(KEY_SALARY))

    return await employe_repo.create(EmployeeSchemasCreate(**create_data))


async def load_database(data: dict[str, list[str]]) -> None:  # noqa
    async with AsyncSessionLocal() as session:
        positions = data[KEY_POSITION]
        depatments = data[KEY_DEPARTMENT]
        statuses = data[KEY_STATUS]

        for position in set(positions):
            await load_position(session, position)
        for depatment in set(depatments):
            await load_division(session, depatment)
        for status in set(statuses):
            await load_status(session, status)

        divisions = data[KEY_DIVISION]

        division_to_department = {}
        for i in range(len(divisions)):
            division = divisions[i]
            if not division:
                continue
            division_to_department[division] = depatment
        for division, department in division_to_department.items():
            await load_division(
                session, division_name=division, department_name=department
            )

        len_data = len(positions)

        managers = {
            data[KEY_MANAGER][i]: None
            for i in range(len_data)
            if data[KEY_MANAGER][i]
        }
        for i in range(len_data):
            value = data[KEY_MANAGER][i]

            if data[KEY_FULL_NAME][i] not in managers:
                continue

            data_employee = {
                KEY_DEPARTMENT: data[KEY_DEPARTMENT][i],
                KEY_DIVISION: data[KEY_DIVISION][i],
                KEY_POSITION: data[KEY_POSITION][i],
                KEY_MANAGER: data[KEY_MANAGER][i],
                KEY_FULL_NAME: data[KEY_FULL_NAME][i],
                KEY_DATE_ADD_WORK: data[KEY_DATE_ADD_WORK][i],
                KEY_DATE_REMOWE_WORK: data[KEY_DATE_REMOWE_WORK][i],
                KEY_STATUS: data[KEY_STATUS][i],
                KEY_STAFF: data[KEY_STAFF][i],
                KEY_SALARY: data[KEY_SALARY][i],
            }
            employe = await load_employee(session, data_employee)
            managers[data[KEY_FULL_NAME][i]] = employe.id

        for i in range(len_data):
            value = data[KEY_MANAGER][i]

            if not value:
                continue

            data_employee = {
                KEY_DEPARTMENT: data[KEY_DEPARTMENT][i],
                KEY_DIVISION: data[KEY_DIVISION][i],
                KEY_POSITION: data[KEY_POSITION][i],
                KEY_MANAGER: data[KEY_MANAGER][i],
                KEY_FULL_NAME: data[KEY_FULL_NAME][i],
                KEY_DATE_ADD_WORK: data[KEY_DATE_ADD_WORK][i],
                KEY_DATE_REMOWE_WORK: data[KEY_DATE_REMOWE_WORK][i],
                KEY_STATUS: data[KEY_STATUS][i],
                KEY_STAFF: data[KEY_STAFF][i],
                KEY_SALARY: data[KEY_SALARY][i],
            }
            manager_id = managers[data[KEY_MANAGER][i]]
            employe = await load_employee(session, data_employee, manager_id)
