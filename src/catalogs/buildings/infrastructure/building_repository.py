from geoalchemy2 import Geography
from sqlalchemy import cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from src.catalogs.buildings.domain.building_entity import BoundsSearchCriteria, BuildingEntity, RadiusSearchCriteria
from src.catalogs.buildings.domain.ibuilding_repository import IBuildingRepository
from src.catalogs.buildings.infrastructure.building_mapper import BuildingMapper
from src.catalogs.buildings.infrastructure.building_model import BuildingModel


class BuildingRepository(IBuildingRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, building_id: UUID) -> BuildingEntity | None:
        model = await self._session.get(BuildingModel, building_id)
        return BuildingMapper.to_domain(model=model) if model else None

    async def get_all_paginated(self, offset: int, limit: int) -> list[BuildingEntity]:
        query = select(BuildingModel).order_by(BuildingModel.address).offset(offset).limit(limit)
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [BuildingMapper.to_domain(m) for m in models]

    async def save(self, building_param: BuildingEntity) -> BuildingEntity:
        model = BuildingMapper.to_model(building_param)
        self._session.add(model)

        try:
            await self._session.commit()
            return BuildingMapper.to_domain(model)
        except Exception:
            await self._session.rollback()
            raise

    async def get_in_radius(self, search_params: RadiusSearchCriteria) -> list[BuildingEntity]:
        point = func.ST_SetSRID(func.ST_MakePoint(search_params.longitude, search_params.latitude), 4326)
        query = select(BuildingModel).where(
            func.ST_DWithin(
                cast(BuildingModel.coordinates, Geography), cast(point, Geography), search_params.radius_meters
            )
        )

        result = await self._session.execute(query)
        models = result.scalars().all()
        return [BuildingMapper.to_domain(m) for m in models]

    async def get_in_bounds(self, search_params: BoundsSearchCriteria) -> list[BuildingEntity]:
        envelope = func.ST_MakeEnvelope(
            search_params.min_lon,
            search_params.min_lat,
            search_params.max_lon,
            search_params.max_lat,
            4326,
        )

        query = select(BuildingModel).where(func.ST_Intersects(BuildingModel.coordinates, envelope))
        result = await self._session.execute(query)
        return [BuildingMapper.to_domain(m) for m in result.scalars().all()]
