from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Index, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import UUID

from src.core.db.base import Base


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    coordinates: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_buildings_address", "address"),
        Index("idx_buildings_coordinates", "coordinates", postgresql_using="gist"),
    )
