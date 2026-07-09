from datetime import datetime, time

from app.domain.enums.fitness_level import FitnessLevel
from app.domain.enums.workout_type import WorkoutType
from app.presentation.schemas.common import BaseSchema


class FitnessProfileResponse(BaseSchema):
    id: int
    user_id: int
    fitness_level: FitnessLevel
    preferred_workouts: list[WorkoutType]
    bio: str | None
    preferred_time_start: time | None
    preferred_time_end: time | None
    is_seeking_partner: bool
    created_at: datetime | None = None


class FitnessProfileCreateRequest(BaseSchema):
    fitness_level: FitnessLevel
    preferred_workouts: list[WorkoutType]
    bio: str | None = None
    preferred_time_start: time | None = None
    preferred_time_end: time | None = None
    is_seeking_partner: bool = True
