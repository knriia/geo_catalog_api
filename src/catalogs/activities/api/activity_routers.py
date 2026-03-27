from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status

from src.catalogs.activities.activity_service import ActivityService
from src.catalogs.activities.api.activity_dto import ActivityCreateRequest, ActivityResponse
from src.catalogs.activities.domain.activity_entity import ActivityCreateEntity
from src.core.types import UUIDv7

activity_router = APIRouter(prefix="/activities", tags=["Activities"])


@activity_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_activity(
    query_params: ActivityCreateRequest,
    service: FromDishka[ActivityService],
) -> ActivityResponse:
    activity_param = ActivityCreateEntity(name=query_params.name, parent_id=query_params.parent_id)
    activity = await service.create_activity(activity_param=activity_param)
    return ActivityResponse.model_validate(activity)


@activity_router.get("/tree/{activity_id}")
@inject
async def get_activity_branch(
    activity_id: UUIDv7,
    service: FromDishka[ActivityService],
) -> list[ActivityResponse]:
    activities = await service.get_full_tree(activity_id=activity_id)
    return [ActivityResponse.model_validate(b) for b in activities]


@activity_router.get("/")
@inject
async def get_all_activities(
    *,
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Размер страницы")] = 20,
    service: FromDishka[ActivityService],
) -> list[ActivityResponse]:
    offset = (page - 1) * size
    activities = await service.get_all_paginated(offset, size)
    return [ActivityResponse.model_validate(b) for b in activities]
