from abc import ABC, abstractmethod

from uuid6 import UUID

from src.business.organizations.domain.organization_entity import OrganizationEntity


class IOrganizationRepository(ABC):
    @abstractmethod
    async def save(self, entity: OrganizationEntity) -> OrganizationEntity:
        pass

    @abstractmethod
    async def get_by_id(self, org_id: UUID) -> OrganizationEntity | None:
        pass

    @abstractmethod
    async def get_all_paginated(self, offset: int, limit: int) -> list[OrganizationEntity]:
        pass

    @abstractmethod
    async def get_by_building_id(self, building_id: UUID) -> list[OrganizationEntity]:
        pass

    @abstractmethod
    async def get_by_building_ids(self, building_ids: list[UUID]) -> list[OrganizationEntity]:
        pass

    @abstractmethod
    async def get_by_activity_ids(self, activity_ids: list[UUID]) -> list[OrganizationEntity]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> list[OrganizationEntity]:
        pass
