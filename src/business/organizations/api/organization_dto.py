from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from src.core.types import UUIDv7

if TYPE_CHECKING:
    from src.business.organizations.domain.organization_entity import OrganizationEntity
    from src.catalogs.activities.domain.activity_entity import ActivityEntity
    from src.catalogs.buildings.domain.building_entity import BuildingEntity


class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, examples=["ООО Рога и Копыта"])
    building_id: UUIDv7 = Field(..., examples=["018e3e4a-5f12-7abc-bf21-9958362b535d"])
    phone_numbers: list[str] = Field(..., min_length=1, examples=["89991234567", "8-923-666-13-13"])
    activity_ids: list[UUIDv7] = Field(..., examples=["018e3e4a-5f12-7abc-bf21-9958362b535d"])


class ActivityBriefResponse(BaseModel):
    id: UUIDv7
    name: str

    @classmethod
    def from_entity(cls, activity: "ActivityEntity") -> "ActivityBriefResponse":
        return cls(id=activity.id, name=activity.name)


class BuildingBriefResponse(BaseModel):
    id: UUIDv7
    address: str

    @classmethod
    def from_entity(cls, building: "BuildingEntity") -> "BuildingBriefResponse":
        return cls(id=building.id, address=building.address)


class OrganizationResponse(BaseModel):
    id: UUIDv7
    name: str
    phone_numbers: list[str] = Field(..., min_length=1)

    building: BuildingBriefResponse
    activities: list[ActivityBriefResponse]

    model_config = ConfigDict(from_attributes=True, frozen=True)

    @classmethod
    def from_entity(cls, org: "OrganizationEntity") -> "OrganizationResponse":
        return cls(
            id=org.id,
            name=org.name,
            phone_numbers=org.phone_numbers,
            building=BuildingBriefResponse.from_entity(org.building) if org.building else None,
            activities=[ActivityBriefResponse.from_entity(a) for a in org.activities],
        )
