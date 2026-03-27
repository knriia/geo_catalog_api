from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.core.types import UUIDv7


class BuildingCreateRequest(BaseModel):
    address: str = Field(..., min_length=5, max_length=255, examples=["г. Москва, ул. Ленина 1, офис 3"])
    latitude: float = Field(..., ge=-90, le=90, examples=[55.7558])
    longitude: float = Field(..., ge=-180, le=180, examples=[37.6173])


class BuildingSearchRadiusRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, examples=[55.75222])
    longitude: float = Field(..., ge=-180, le=180, examples=[37.59747])
    radius_meters: float = Field(..., gt=0, le=1000000, examples=[5000])


class BuildingSearchBoundsRequest(BaseModel):
    min_latitude: float = Field(..., ge=-90, le=90, examples=[55.0])
    min_longitude: float = Field(..., ge=-180, le=180, examples=[37.0])
    max_latitude: float = Field(..., ge=-90, le=90, examples=[56.0])
    max_longitude: float = Field(..., ge=-180, le=180, examples=[38.0])

    @model_validator(mode="after")
    def validate_bounds(self) -> "BuildingSearchBoundsRequest":
        if self.min_latitude >= self.max_latitude:
            raise ValueError("min_latitude must be less than max_latitude")
        if self.min_longitude >= self.max_longitude:
            raise ValueError("min_longitude must be less than max_longitude")
        return self


class BuildingResponse(BaseModel):
    id: UUIDv7
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True, frozen=True)
