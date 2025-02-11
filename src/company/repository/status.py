from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import Status
from database import get_async_session
from repository import RepositoryBase


class StatusRepository(RepositoryBase):
    """/."""


async def get_status_repo(
    session: AsyncSession = Depends(get_async_session)
) -> StatusRepository:
    return StatusRepository(Status, session)
