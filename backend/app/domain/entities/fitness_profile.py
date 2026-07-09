from dataclasses import dataclass, field
from datetime import datetime, time

from app.domain.enums.fitness_level import FitnessLevel
from app.domain.enums.workout_type import WorkoutType


@dataclass
class FitnessProfile:
    id: int | None
    user_id: int
    fitness_level: FitnessLevel
    preferred_workouts: list[WorkoutType] = field(default_factory=list)
    bio: str | None = None
    preferred_time_start: time | None = None
    preferred_time_end: time | None = None
    is_seeking_partner: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
