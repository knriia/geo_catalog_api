from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import uuid6
from uuid6 import UUID

if TYPE_CHECKING:
    from src.catalogs.activities.domain.activity_entity import ActivityEntity
    from src.catalogs.buildings.domain.building_entity import BuildingEntity


@dataclass(frozen=True)
class OrganizationCreateEntity:
    name: str
    building_id: UUID
    phone_numbers: list[str]
    activity_ids: list[UUID]

    def create_organization_entity(self) -> "OrganizationEntity":
        return OrganizationEntity(
            id=uuid6.uuid7(),
            name=self.name,
            building_id=self.building_id,
            phone_numbers=self.phone_numbers,
            activity_ids=self.activity_ids,
        )


@dataclass(kw_only=True)
class OrganizationEntity:
    id: UUID
    name: str
    building_id: UUID
    phone_numbers: list[str] = field(default_factory=list)
    activity_ids: list[UUID] = field(default_factory=list)

    building: Optional["BuildingEntity"] = None
    activities: list["ActivityEntity"] = field(default_factory=list)
