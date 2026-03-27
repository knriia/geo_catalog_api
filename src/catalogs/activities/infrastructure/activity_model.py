from typing import Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import UUID

from src.core.db.base import Base


class ActivityModel(Base):
    __tablename__ = "activities"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    parent_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
    )
    level: Mapped[int] = mapped_column(default=1)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    parent: Mapped[Optional["ActivityModel"]] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list["ActivityModel"]] = relationship(back_populates="parent", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_activities_path", "path"),)
