from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.catalogs.activities.activity_service import ActivityService
from src.catalogs.activities.domain.iactivity_repository import IActivityRepository
from src.catalogs.activities.infrastructure.activity_repository import ActivityRepository


class ActivityProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_activity_repository(self, session: AsyncSession) -> IActivityRepository:
        return ActivityRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_activity_service(self, activity_repository: IActivityRepository) -> ActivityService:
        return ActivityService(activity_repository=activity_repository)
