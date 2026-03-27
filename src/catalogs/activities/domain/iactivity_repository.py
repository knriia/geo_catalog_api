from abc import ABC, abstractmethod

from uuid6 import UUID

from src.catalogs.activities.domain.activity_entity import ActivityEntity


class IActivityRepository(ABC):
    @abstractmethod
    async def get_by_id(self, activity_id: UUID) -> ActivityEntity | None:
        pass

    @abstractmethod
    async def get_all_paginated(self, offset: int, limit: int) -> list[ActivityEntity]:
        pass

    @abstractmethod
    async def get_by_parent(self, parent_id: UUID | None) -> list[ActivityEntity]:
        pass

    @abstractmethod
    async def get_descendants(self, path: str) -> list[ActivityEntity]:
        pass

    @abstractmethod
    async def save(self, activity_entity: ActivityEntity) -> ActivityEntity:
        pass
