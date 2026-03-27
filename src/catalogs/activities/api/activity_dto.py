from pydantic import BaseModel, ConfigDict, Field

from src.core.types import UUIDv7


class ActivityCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, examples=["Мясная продукция"])
    parent_id: UUIDv7 | None


class ActivityResponse(BaseModel):
    id: UUIDv7
    name: str
    parent_id: UUIDv7 | None
    level: int

    model_config = ConfigDict(from_attributes=True, frozen=True)
