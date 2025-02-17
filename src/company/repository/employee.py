from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from company.models import Employee
from database import get_async_session
from repository import RepositoryBase


class EmployeeRepository(RepositoryBase):
    """Employee repostiory."""


async def get_employee_repo(
    session: AsyncSession = Depends(get_async_session),
) -> EmployeeRepository:
    return EmployeeRepository(Employee, session)
