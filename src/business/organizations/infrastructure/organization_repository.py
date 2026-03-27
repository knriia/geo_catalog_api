from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from uuid6 import UUID

from src.business.organizations.domain.iorganization_repository import IOrganizationRepository
from src.business.organizations.domain.organization_entity import OrganizationEntity
from src.business.organizations.infrastructure.organization_mapper import OrganizationMapper
from src.business.organizations.infrastructure.organization_model import OrganizationActivityModel, OrganizationModel


class OrganizationRepository(IOrganizationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _base_query() -> Select:
        return select(OrganizationModel).options(
            joinedload(OrganizationModel.building),
            selectinload(OrganizationModel.activities),
            selectinload(OrganizationModel.phone_numbers),
        )

    async def get_by_id(self, org_id: UUID) -> OrganizationEntity | None:
        stmt = self._base_query().where(OrganizationModel.id == org_id)
        result = await self._session.execute(stmt)
        model = result.scalars().unique().one_or_none()
        return OrganizationMapper.to_domain(model) if model else None

    async def get_all_paginated(self, offset: int, limit: int) -> list[OrganizationEntity]:
        stmt = self._base_query().order_by(OrganizationModel.name).offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        models = result.scalars().unique().all()
        return [OrganizationMapper.to_domain(m) for m in models]

    async def get_by_building_id(self, building_id: UUID) -> list[OrganizationEntity]:
        stmt = self._base_query().where(OrganizationModel.building_id == building_id)
        result = await self._session.execute(stmt)
        models = result.scalars().unique().all()
        return [OrganizationMapper.to_domain(m) for m in models]

    async def get_by_activity_ids(self, activity_ids: list[UUID]) -> list[OrganizationEntity]:
        stmt = (
            self._base_query()
            .join(OrganizationActivityModel)
            .where(OrganizationActivityModel.activity_id.in_(activity_ids))
            .distinct()
        )
        result = await self._session.execute(stmt)
        models = result.scalars().unique().all()
        return [OrganizationMapper.to_domain(m) for m in models]

    async def get_by_building_ids(self, building_ids: list[UUID]) -> list[OrganizationEntity]:
        stmt = self._base_query().where(OrganizationModel.building_id.in_(building_ids))
        result = await self._session.execute(stmt)
        models = result.scalars().unique().all()
        return [OrganizationMapper.to_domain(m) for m in models]

    async def get_by_name(self, name: str) -> list[OrganizationEntity]:
        stmt = self._base_query().where(OrganizationModel.name.ilike(f"%{name}%"))
        result = await self._session.execute(stmt)
        models = result.scalars().unique().all()
        return [OrganizationMapper.to_domain(m) for m in models]

    async def save(self, entity: OrganizationEntity) -> OrganizationEntity:
        model = OrganizationMapper.to_model(entity)
        self._session.add(model)
        try:
            await self._session.commit()
            return await self.get_by_id(model.id)
        except Exception:
            await self._session.rollback()
            raise
