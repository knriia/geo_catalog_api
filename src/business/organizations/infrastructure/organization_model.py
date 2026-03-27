from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import UUID

from src.core.db.base import Base

if TYPE_CHECKING:
    from src.catalogs.activities.infrastructure.activity_model import ActivityModel
    from src.catalogs.buildings.infrastructure.building_model import BuildingModel


class OrganizationActivityModel(Base):
    __tablename__ = "organization_activities"

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    activity_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    organization: Mapped["OrganizationModel"] = relationship(back_populates="activity_links")


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    building_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    building: Mapped["BuildingModel"] = relationship(lazy="raise")

    activities: Mapped[list["ActivityModel"]] = relationship(
        secondary="organization_activities",
        viewonly=True,
        lazy="raise",
    )

    activity_links: Mapped[list["OrganizationActivityModel"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="raise",
    )

    phone_numbers: Mapped[list["OrganizationPhoneModel"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="raise",
    )


class OrganizationPhoneModel(Base):
    __tablename__ = "organization_phones"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    organization: Mapped["OrganizationModel"] = relationship(back_populates="phone_numbers")
