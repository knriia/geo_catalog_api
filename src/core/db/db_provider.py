from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.core.config import Settings
from src.core.db.session_manager import SessionManager


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_manager(self, engine: AsyncEngine) -> AsyncGenerator[SessionManager, None]:
        db_manager = SessionManager(engine=engine)
        yield db_manager
        await db_manager.close()

    @provide(scope=Scope.REQUEST)
    async def get_session(self, db_manager: SessionManager) -> AsyncGenerator[AsyncSession, None]:
        async with db_manager.get_session() as session:
            yield session
