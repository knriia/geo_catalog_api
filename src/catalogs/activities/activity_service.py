from uuid6 import UUID

from src.catalogs.activities.domain.activity_entity import ActivityCreateEntity, ActivityEntity
from src.catalogs.activities.domain.activity_exceptions import ActivityNotFoundError
from src.catalogs.activities.domain.iactivity_repository import IActivityRepository


class ActivityService:
    def __init__(self, activity_repository: IActivityRepository) -> None:
        self._repository = activity_repository

    async def create_activity(self, activity_param: ActivityCreateEntity) -> ActivityEntity:
        if activity_param.parent_id is None:
            activity_entity = activity_param.create_root()
            return await self._repository.save(activity_entity=activity_entity)

        parent = await self.get_activity_by_id(activity_param.parent_id)
        activity_entity = activity_param.create_child(parent)
        return await self._repository.save(activity_entity)

    async def get_activity_by_id(self, activity_id: UUID) -> ActivityEntity:
        activity = await self._repository.get_by_id(activity_id)
        if activity is None:
            raise ActivityNotFoundError(activity_id)
        return activity

    async def get_all_paginated(self, offset: int, limit: int) -> list[ActivityEntity]:
        return await self._repository.get_all_paginated(offset, limit)

    async def get_full_tree(self, activity_id: UUID) -> list[ActivityEntity]:
        root = await self.get_activity_by_id(activity_id)
        descendants = await self._repository.get_descendants(root.path)
        return [root, *descendants]

    async def get_subtree_ids(self, activity_id: UUID) -> list[UUID]:
        tree = await self.get_full_tree(activity_id)
        return [a.id for a in tree]
