from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class EmployeeSchemasCreate(BaseModel):

    first_name: str = Field(
        min_length=1,
        max_length=150,
        title="Fst name",
        description="Имя сотрудника",
    )
    last_name: str = Field(
        min_length=1,
        max_length=150,
        title="Last name",
        description="Фамилия сотрудника",
    )
    middle_name: str = Field(
        min_length=1,
        max_length=150,
        title="Mid name",
        description="Отчество сотрудника",
    )

    hire_date: Optional[date] = Field(
        None, title="Hire date", description="Дата приема на работу."
    )
    termination_date: Optional[date] = Field(
        None, title="Termination date.", description="Дата увольнения."
    )

    is_staff: bool = Field(
        True, title="Is staff", description="Это штатный сотрудник."
    )
    salary: PositiveInt = Field(
        0,
        title="Salary",
        description="Зарботная плата сотрудника, положительное число.",
    )

    manager_id: Optional[int] = Field(
        None, title="Manager id", description="id менеджера в базе данных."
    )

    division_id: Optional[int] = Field(
        None, title="Division id", description="id отдела в базе данных."
    )

    position_id: int = Field(
        title="Position id", description="id должности в базе данных."
    )

    status_id: int = Field(
        title="Status id", description="id Статуса сотрудника в базе данных."
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Иванов",
                "last_name": "Иван",
                "middle_name": "Иванович",
                "hire_date": "2023-02-01",
                "termination_date": None,
                "is_staff": True,
                "salary": 50000,
                "manager_id": None,
                "division_id": 2,
                "position_id": 5,
                "status_id": 1,
            }
        }


class EmployeeSchemasUpdate(EmployeeSchemasCreate):

    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=150,
        title="Fst name",
        description="Имя сотрудника",
    )
    last_name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Last name",
        description="Фамилия сотрудника",
    )
    middle_name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Mid name",
        description="Отчество сотрудника",
    )

    hire_date: Optional[date] = Field(
        None, title="Hire date", description="Дата приема на работу."
    )
    termination_date: Optional[date] = Field(
        None, title="Termination date.", description="Дата увольнения."
    )

    is_staff: Optional[bool] = Field(
        True, title="Is staff", description="Это штатный сотрудник."
    )
    salary: Optional[PositiveInt] = Field(
        0,
        title="Salary",
        description="Зарботная плата сотрудника, положительное число.",
    )

    manager_id: Optional[int] = Field(
        None, title="Manager id", description="id менеджера в базе данных."
    )

    division_id: Optional[int] = Field(
        None, title="Division id", description="id отдела в базе данных."
    )

    position_id: Optional[int] = Field(
        title="Position id", description="id должности в базе данных."
    )

    status_id: Optional[int] = Field(
        title="Status id", description="id Статуса сотрудника в базе данных."
    )


class EmployeeSchemaDB(BaseModel):
    id: int
    first_name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Fst name",
        description="Имя сотрудника",
    )
    last_name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Last name",
        description="Фамилия сотрудника",
    )
    middle_name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Mid name",
        description="Отчество сотрудника",
    )

    hire_date: Optional[date] = Field()
    termination_date: Optional[date] = Field()

    is_staff: Optional[bool] = Field()
    salary: Optional[PositiveInt] = Field()

    manager_id: Optional[int] = Field()

    division_id: Optional[int] = Field()

    position_id: Optional[int] = Field()

    status_id: Optional[int] = Field()

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Иванов",
                "last_name": "Иван",
                "middle_name": "Иванович",
                "hire_date": "2023-02-01",
                "termination_date": None,
                "is_staff": True,
                "salary": 50000,
                "manager_id": None,
                "division_id": 2,
                "position_id": 5,
                "status_id": 1,
            }
        }
