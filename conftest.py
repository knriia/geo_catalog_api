from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from dishka import AsyncContainer, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from src.business.organizations.infrastructure.organization_provider import OrganizationProvider
from src.catalogs.activities.infrastructure.activity_provider import ActivityProvider
from src.catalogs.buildings.infrastructure.building_provider import BuildingProvider
from src.core.config import Settings
from src.core.db.base import Base
from src.core.db.db_provider import DBProvider
from src.main import app


class TestDBProvider(DBProvider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        settings = Settings()
        settings.DB_NAME = f"{settings.DB_NAME}_test"
        return settings

    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(settings.database_url, poolclass=NullPool)
        yield engine
        await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def container():
    container = make_async_container(TestDBProvider(), ActivityProvider(), BuildingProvider(), OrganizationProvider())

    engine: Any = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(Base.metadata.create_all)

    yield container

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await container.close()


@pytest_asyncio.fixture(scope="session")
async def client(container: AsyncContainer) -> AsyncGenerator[AsyncClient, None]:
    setup_dishka(container, app)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        settings = await container.get(Settings)
        ac.headers.update({"X-API-KEY": settings.STATIC_API_KEY.get_secret_value()})
        yield ac
