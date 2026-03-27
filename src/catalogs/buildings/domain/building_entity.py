from dataclasses import dataclass

from uuid6 import UUID, uuid7


@dataclass(kw_only=True)
class BuildingCreateEntity:
    address: str
    latitude: float
    longitude: float

    def create_building_entity(self) -> "BuildingEntity":
        return BuildingEntity(id=uuid7(), address=self.address, latitude=self.latitude, longitude=self.longitude)


@dataclass(kw_only=True)
class BuildingEntity:
    id: UUID
    address: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class RadiusSearchCriteria:
    latitude: float
    longitude: float
    radius_meters: float


@dataclass(frozen=True)
class BoundsSearchCriteria:
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float
