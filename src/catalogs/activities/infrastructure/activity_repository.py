from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from src.catalogs.activities.domain.activity_entity import ActivityEntity
from src.catalogs.activities.domain.iactivity_repository import IActivityRepository
from src.catalogs.activities.infrastructure.activity_mapper import ActivityMapper
from src.catalogs.activities.infrastructure.activity_model import ActivityModel


class ActivityRepository(IActivityRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, activity_id: UUID) -> ActivityEntity | None:
        model = await self._session.get(ActivityModel, activity_id)
        return ActivityMapper.to_domain(model=model) if model else None

    async def get_all_paginated(self, offset: int, limit: int) -> list[ActivityEntity]:
        query = select(ActivityModel).order_by(ActivityModel.level, ActivityModel.name).offset(offset).limit(limit)
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [ActivityMapper.to_domain(m) for m in models]

    async def get_by_parent(self, parent_id: UUID | None) -> list[ActivityEntity]:
        query = select(ActivityModel).where(ActivityModel.parent_id == parent_id)
        result = await self._session.execute(query)
        return [ActivityMapper.to_domain(m) for m in result.scalars().all()]

    async def _get_model_by_id(self, activity_id: UUID) -> ActivityModel | None:
        return await self._session.get(ActivityModel, activity_id)

    async def get_descendants(self, path: str) -> list[ActivityEntity]:
        stmt = select(ActivityModel).where(ActivityModel.path.like(f"{path}.%"))
        result = await self._session.execute(stmt)
        return [ActivityMapper.to_domain(m) for m in result.scalars().all()]

    async def save(self, activity_entity: ActivityEntity) -> ActivityEntity:
        model = ActivityMapper.to_model(activity_entity)
        self._session.add(model)

        try:
            await self._session.commit()
            return ActivityMapper.to_domain(model)
        except Exception:
            await self._session.rollback()
            raise
