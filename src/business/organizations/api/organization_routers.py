from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status

from src.business.organizations.api.organization_dto import OrganizationCreateRequest, OrganizationResponse
from src.business.organizations.domain.organization_entity import OrganizationCreateEntity
from src.business.organizations.organization_service import OrganizationService
from src.core.types import UUIDv7

organization_router = APIRouter(prefix="/organizations", tags=["Organizations"])


@organization_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_organization(
    request: OrganizationCreateRequest,
    service: FromDishka[OrganizationService],
) -> OrganizationResponse:
    entity = OrganizationCreateEntity(
        name=request.name,
        building_id=request.building_id,
        phone_numbers=request.phone_numbers,
        activity_ids=request.activity_ids,
    )
    organization = await service.create_organization(entity)
    return OrganizationResponse.from_entity(organization)


@organization_router.get("/search/name")
@inject
async def search_by_name(
    *,
    name: Annotated[str, Query(min_length=2)],
    service: FromDishka[OrganizationService],
) -> list[OrganizationResponse]:
    organizations = await service.search_by_name(name)
    return [OrganizationResponse.from_entity(b) for b in organizations]


@organization_router.get("/search/activity/{activity_id}")
@inject
async def search_by_activity(
    activity_id: UUIDv7,
    service: FromDishka[OrganizationService],
) -> list[OrganizationResponse]:
    organizations = await service.search_by_activity(activity_id)
    return [OrganizationResponse.from_entity(b) for b in organizations]


@organization_router.get("/search/radius")
@inject
async def search_by_radius(
    *,
    lat: Annotated[float, Query(ge=-90, le=90)],
    lon: Annotated[float, Query(ge=-180, le=180)],
    radius: Annotated[float, Query(gt=0)],
    service: FromDishka[OrganizationService],
) -> list[OrganizationResponse]:
    organizations = await service.search_in_radius(lat, lon, radius)
    return [OrganizationResponse.from_entity(b) for b in organizations]


@organization_router.get("/search/bounds")
@inject
async def search_by_bounds(
    *,
    min_lat: Annotated[float, Query(ge=-90, le=90, description="Нижняя широта")],
    min_lon: Annotated[float, Query(ge=-180, le=180, description="Левая долгота")],
    max_lat: Annotated[float, Query(ge=-90, le=90, description="Верхняя широта")],
    max_lon: Annotated[float, Query(ge=-180, le=180, description="Правая долгота")],
    service: FromDishka[OrganizationService],
) -> list[OrganizationResponse]:
    organizations = await service.search_in_bounds(min_lat=min_lat, min_lon=min_lon, max_lat=max_lat, max_lon=max_lon)
    return [OrganizationResponse.from_entity(b) for b in organizations]


@organization_router.get("/building/{building_id}")
@inject
async def get_by_building(building_id: UUIDv7, service: FromDishka[OrganizationService]) -> list[OrganizationResponse]:
    organizations = await service.get_organization_by_building(building_id)
    return [OrganizationResponse.from_entity(b) for b in organizations]


@organization_router.get("/")
@inject
async def get_all_organizations(
    *,
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Размер страницы")] = 20,
    service: FromDishka[OrganizationService],
) -> list[OrganizationResponse]:
    offset = (page - 1) * size
    organizations = await service.get_all_paginated(offset, size)
    return [OrganizationResponse.from_entity(b) for b in organizations]


@organization_router.get("/{org_id}")
@inject
async def get_organization(org_id: UUIDv7, service: FromDishka[OrganizationService]) -> OrganizationResponse:
    organization = await service.get_organization(org_id)
    return OrganizationResponse.from_entity(organization)
