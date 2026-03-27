from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Query

from src.catalogs.buildings.api.building_dto import (
    BuildingCreateRequest,
    BuildingResponse,
    BuildingSearchBoundsRequest,
    BuildingSearchRadiusRequest,
)
from src.catalogs.buildings.building_service import BuildingService
from src.catalogs.buildings.domain.building_entity import BuildingCreateEntity
from src.core.types import UUIDv7

building_router = APIRouter(prefix="/buildings", tags=["Buildings"])


@building_router.post("/", status_code=201)
@inject
async def create_building(
    query_params: BuildingCreateRequest,
    service: FromDishka[BuildingService],
) -> BuildingResponse:
    building_param = BuildingCreateEntity(
        address=query_params.address,
        latitude=query_params.latitude,
        longitude=query_params.longitude,
    )
    building = await service.create_building(building_param=building_param)
    return BuildingResponse.model_validate(building)


@building_router.get("/")
@inject
async def get_buildings(
    *,
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Размер страницы")] = 20,
    service: FromDishka[BuildingService],
) -> list[BuildingResponse]:
    offset = (page - 1) * size
    buildings = await service.get_all_paginated(offset, size)
    return [BuildingResponse.model_validate(b) for b in buildings]


@building_router.get("/{building_id}")
@inject
async def get_building(*, building_id: UUIDv7, service: FromDishka[BuildingService]) -> BuildingResponse:
    building = await service.get_building(building_id)
    return BuildingResponse.model_validate(building)


@building_router.get("/search/radius")
@inject
async def search_by_radius(
    query_params: Annotated[BuildingSearchRadiusRequest, Depends()],
    service: FromDishka[BuildingService],
) -> list[BuildingResponse]:
    buildings = await service.search_in_radius(
        lat=query_params.latitude,
        lon=query_params.longitude,
        radius=query_params.radius_meters,
    )
    return [BuildingResponse.model_validate(b) for b in buildings]


@building_router.get("/search/bounds")
@inject
async def search_by_bounds(
    query_params: Annotated[BuildingSearchBoundsRequest, Depends()],
    service: FromDishka[BuildingService],
) -> list[BuildingResponse]:
    buildings = await service.search_in_bounds(
        min_lat=query_params.min_latitude,
        min_lon=query_params.min_longitude,
        max_lat=query_params.max_latitude,
        max_lon=query_params.max_longitude,
    )
    return [BuildingResponse.model_validate(b) for b in buildings]
