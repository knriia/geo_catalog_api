from abc import ABC, abstractmethod

from uuid6 import UUID

from src.catalogs.buildings.domain.building_entity import BoundsSearchCriteria, BuildingEntity, RadiusSearchCriteria


class IBuildingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, building_id: UUID) -> BuildingEntity | None:
        pass

    @abstractmethod
    async def get_all_paginated(self, offset: int, limit: int) -> list[BuildingEntity]:
        pass

    @abstractmethod
    async def save(self, building_param: BuildingEntity) -> BuildingEntity:
        pass

    @abstractmethod
    async def get_in_radius(self, search_params: RadiusSearchCriteria) -> list[BuildingEntity]:
        pass

    @abstractmethod
    async def get_in_bounds(self, search_params: BoundsSearchCriteria) -> list[BuildingEntity]:
        pass
