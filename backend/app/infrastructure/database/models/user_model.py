from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.user_role import UserRole
from app.infrastructure.database.base import Base, TimestampMixin


class UserModel(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default=UserRole.RESIDENT.value)
    community_id: Mapped[int] = mapped_column(ForeignKey("communities.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    community = relationship("CommunityModel", back_populates="users")
    fitness_profile = relationship("FitnessProfileModel", back_populates="user", uselist=False)
    bookings = relationship("BookingModel", back_populates="user")
    notifications = relationship("NotificationModel", back_populates="user")
