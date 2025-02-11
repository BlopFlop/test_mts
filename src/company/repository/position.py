from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import Position
from database import get_async_session
from repository import RepositoryBase


class PositionRepository(RepositoryBase):
    """/."""


async def get_position_repo(
    session: AsyncSession = Depends(get_async_session)
) -> PositionRepository:
    return PositionRepository(Position, session)
