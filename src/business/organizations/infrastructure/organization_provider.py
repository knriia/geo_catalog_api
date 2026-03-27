from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.organizations.domain.iorganization_repository import IOrganizationRepository
from src.business.organizations.infrastructure.organization_repository import OrganizationRepository
from src.business.organizations.organization_service import OrganizationService
from src.catalogs.activities.activity_service import ActivityService
from src.catalogs.buildings.building_service import BuildingService


class OrganizationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_repository(self, session: AsyncSession) -> IOrganizationRepository:
        return OrganizationRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_service(
        self,
        repository: IOrganizationRepository,
        activity_service: ActivityService,
        building_service: BuildingService,
    ) -> OrganizationService:
        return OrganizationService(repository, activity_service, building_service)
