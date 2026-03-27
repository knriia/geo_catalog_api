from dataclasses import dataclass

from uuid6 import UUID, uuid7

from src.catalogs.activities.domain.activity_exceptions import ActivityLimitError


@dataclass(frozen=True)
class ActivityCreateEntity:
    name: str
    parent_id: UUID | None = None

    @staticmethod
    def _validate_parent(parent: "ActivityEntity") -> None:
        if parent.level >= 3:
            raise ActivityLimitError()

    @staticmethod
    def _generate_id() -> UUID:
        return uuid7()

    def create_root(self) -> "ActivityEntity":
        new_id = self._generate_id()
        return ActivityEntity(id=new_id, name=self.name, parent_id=None, level=1, path=str(new_id))

    def create_child(self, parent: "ActivityEntity") -> "ActivityEntity":
        self._validate_parent(parent)

        new_id = self._generate_id()
        return ActivityEntity(
            id=new_id,
            name=self.name,
            parent_id=parent.id,
            level=parent.level + 1,
            path=f"{parent.path}.{new_id}",
        )


@dataclass(kw_only=True)
class ActivityEntity:
    id: UUID
    name: str
    parent_id: UUID | None = None
    level: int
    path: str
