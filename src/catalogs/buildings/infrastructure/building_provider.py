from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.catalogs.buildings.building_service import BuildingService
from src.catalogs.buildings.domain.ibuilding_repository import IBuildingRepository
from src.catalogs.buildings.infrastructure.building_repository import BuildingRepository


class BuildingProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_repository(self, session: AsyncSession) -> IBuildingRepository:
        return BuildingRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_service(self, repository: IBuildingRepository) -> BuildingService:
        return BuildingService(repository)
