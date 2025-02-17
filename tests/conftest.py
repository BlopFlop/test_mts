from pathlib import Path
from typing import Callable

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from src.company.repository import (
    get_division_repo,
    get_employee_repo,
    get_position_repo,
    get_status_repo,
)
from src.company.schemas import (
    DivisionSchemaCreate,
    EmployeeSchemasCreate,
    PositionSchemaCreate,
    StatusSchemaCreate,
)
from src.config import test_database_config
from src.database import Base, get_async_session
from src.main import app

engine_test = create_async_engine(
    test_database_config.database_url, poolclass=NullPool
)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base.metadata.bind = engine_test

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


async def override_db():
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(loop_scope="session", scope="module", autouse=True)
async def init_db():
    yield
    async with engine_test.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        conn.commit()


@pytest.fixture(scope="session")
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    with TestClient(app) as client:
        yield client


async def create_mock_elt(
    session: AsyncSession,
    search_field: str,
    create_schema: BaseModel,
    repo_func: Callable,
):
    repo = await repo_func(session)
    data = await repo.get_obj_for_field_arg(
        search_field, getattr(create_schema, search_field), many=False
    )
    if not data:
        data = await repo.create(create_schema)
    await session.aclose()
    return data


@pytest.mark.asyncio
@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def division():
    session = await override_db().__anext__()
    data = {"name": "Parent Department", "parent_id": None}
    division_schema = DivisionSchemaCreate(**data)

    return await create_mock_elt(
        session, "name", division_schema, get_division_repo
    )


@pytest.mark.asyncio
@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def status():
    session = await override_db().__anext__()
    data = {"name": "Отпуск"}
    status_schema = StatusSchemaCreate(**data)

    return await create_mock_elt(
        session, "name", status_schema, get_status_repo
    )


@pytest.mark.asyncio
@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def position():
    session = await override_db().__anext__()
    data = {"name": "Менеджер"}
    position_schema = PositionSchemaCreate(**data)

    return await create_mock_elt(
        session, "name", position_schema, get_position_repo
    )
