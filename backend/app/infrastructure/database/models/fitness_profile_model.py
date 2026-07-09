import json

from sqlalchemy import Boolean, ForeignKey, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, TimestampMixin


class FitnessProfileModel(Base, TimestampMixin):
    __tablename__ = "fitness_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    fitness_level: Mapped[str] = mapped_column(String(20), nullable=False)
    preferred_workouts: Mapped[str] = mapped_column(Text, default="[]")
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferred_time_start: Mapped[str | None] = mapped_column(Time, nullable=True)
    preferred_time_end: Mapped[str | None] = mapped_column(Time, nullable=True)
    is_seeking_partner: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("UserModel", back_populates="fitness_profile")

    @property
    def workouts_list(self) -> list[str]:
        return json.loads(self.preferred_workouts or "[]")

    @workouts_list.setter
    def workouts_list(self, value: list[str]) -> None:
        self.preferred_workouts = json.dumps(value)
