from uuid6 import UUID

from src.business.organizations.domain.iorganization_repository import IOrganizationRepository
from src.business.organizations.domain.organization_entity import OrganizationCreateEntity, OrganizationEntity
from src.business.organizations.domain.organization_exceptions import OrganizationNotFoundError
from src.catalogs.activities.activity_service import ActivityService
from src.catalogs.buildings.building_service import BuildingService


class OrganizationService:
    def __init__(
        self,
        repository: IOrganizationRepository,
        activity_service: ActivityService,
        building_service: BuildingService,
    ):
        self._repository = repository
        self._activity_service = activity_service
        self._building_service = building_service

    async def create_organization(self, organization_params: OrganizationCreateEntity) -> OrganizationEntity:
        return await self._repository.save(organization_params.create_organization_entity())

    async def get_organization_by_building(self, building_id: UUID) -> list[OrganizationEntity]:
        return await self._repository.get_by_building_id(building_id)

    async def search_by_activity(self, activity_id: UUID) -> list[OrganizationEntity]:
        target_activity_ids = await self._activity_service.get_subtree_ids(activity_id)
        return await self._repository.get_by_activity_ids(target_activity_ids)

    async def get_all_paginated(self, offset: int, limit: int) -> list[OrganizationEntity]:
        return await self._repository.get_all_paginated(offset, limit)

    async def search_in_radius(self, lat: float, lon: float, radius: float) -> list[OrganizationEntity]:
        buildings = await self._building_service.search_in_radius(lat=lat, lon=lon, radius=radius)
        if not buildings:
            return []

        building_ids = [b.id for b in buildings]
        return await self._repository.get_by_building_ids(building_ids)

    async def search_in_bounds(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
    ) -> list[OrganizationEntity]:
        buildings = await self._building_service.search_in_bounds(min_lat, min_lon, max_lat, max_lon)
        if not buildings:
            return []

        building_ids = [b.id for b in buildings]
        return await self._repository.get_by_building_ids(building_ids)

    async def search_by_name(self, name: str) -> list[OrganizationEntity]:
        return await self._repository.get_by_name(name)

    async def get_organization(self, org_id: UUID) -> OrganizationEntity:
        organization = await self._repository.get_by_id(org_id)
        if organization is None:
            raise OrganizationNotFoundError(org_id)
        return organization
