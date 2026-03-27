from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator


def check_uuid7(v: UUID) -> UUID:
    if v.version != 7:
        raise ValueError("UUID must be version 7")
    return v


UUIDv7 = Annotated[UUID, AfterValidator(check_uuid7)]
