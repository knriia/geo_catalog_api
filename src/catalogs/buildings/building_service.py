from uuid6 import UUID

from src.catalogs.buildings.domain.building_entity import (
    BoundsSearchCriteria,
    BuildingCreateEntity,
    BuildingEntity,
    RadiusSearchCriteria,
)
from src.catalogs.buildings.domain.building_exceptions import BuildingNotFoundError
from src.catalogs.buildings.domain.ibuilding_repository import IBuildingRepository


class BuildingService:
    def __init__(self, repository: IBuildingRepository):
        self._repository = repository

    async def get_building(self, building_id: UUID) -> BuildingEntity:
        building = await self._repository.get_by_id(building_id)
        if building is None:
            raise BuildingNotFoundError(building_id)
        return building

    async def get_all_paginated(self, offset: int, limit: int) -> list[BuildingEntity]:
        return await self._repository.get_all_paginated(offset, limit)

    async def create_building(self, building_param: BuildingCreateEntity) -> BuildingEntity:
        building_entity = building_param.create_building_entity()
        return await self._repository.save(building_param=building_entity)

    async def search_in_radius(self, lat: float, lon: float, radius: float) -> list[BuildingEntity]:
        search_params = RadiusSearchCriteria(latitude=lat, longitude=lon, radius_meters=radius)
        return await self._repository.get_in_radius(search_params=search_params)

    async def search_in_bounds(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
    ) -> list[BuildingEntity]:
        search_params = BoundsSearchCriteria(min_lat=min_lat, min_lon=min_lon, max_lat=max_lat, max_lon=max_lon)
        return await self._repository.get_in_bounds(search_params=search_params)
