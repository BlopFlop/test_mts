from typing import Coroutine

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from company.models import Division
from database import get_async_session
from repository import RepositoryBase


class DivisionRepository(RepositoryBase):
    """/."""


async def get_division_repo(
    session: AsyncSession = Depends(get_async_session)
) -> RepositoryBase:
    return DivisionRepository(Division, session)
