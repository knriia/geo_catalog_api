from dishka import AsyncContainer, make_async_container

from src.business.organizations.infrastructure.organization_provider import OrganizationProvider
from src.catalogs.activities.infrastructure.activity_provider import ActivityProvider
from src.catalogs.buildings.infrastructure.building_provider import BuildingProvider
from src.core.db.db_provider import DBProvider


def get_di_container() -> AsyncContainer:
    return make_async_container(
        DBProvider(),
        ActivityProvider(),
        BuildingProvider(),
        OrganizationProvider(),
    )
