from datetime import time

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, Time as SATime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, TimestampMixin


class AmenityModel(Base, TimestampMixin):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community_id: Mapped[int] = mapped_column(ForeignKey("communities.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    amenity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=1)
    open_time: Mapped[time] = mapped_column(SATime, nullable=False)
    close_time: Mapped[time] = mapped_column(SATime, nullable=False)
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    community = relationship("CommunityModel", back_populates="amenities")
    bookings = relationship("BookingModel", back_populates="amenity")
