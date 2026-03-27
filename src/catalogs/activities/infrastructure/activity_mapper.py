from src.catalogs.activities.domain.activity_entity import ActivityEntity
from src.catalogs.activities.infrastructure.activity_model import ActivityModel


class ActivityMapper:
    @staticmethod
    def to_domain(model: ActivityModel) -> ActivityEntity:
        return ActivityEntity(
            id=model.id,
            name=model.name,
            parent_id=model.parent_id,
            level=model.level,
            path=model.path,
        )

    @staticmethod
    def to_model(entity: ActivityEntity) -> ActivityModel:
        return ActivityModel(
            id=entity.id,
            name=entity.name,
            parent_id=entity.parent_id,
            level=entity.level,
            path=entity.path,
        )
