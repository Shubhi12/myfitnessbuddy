from abc import ABC, abstractmethod

from app.domain.entities.fitness_profile import FitnessProfile
from app.domain.enums.workout_type import WorkoutType


class FitnessProfileRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> FitnessProfile | None:
        ...

    @abstractmethod
    async def create(self, profile: FitnessProfile) -> FitnessProfile:
        ...

    @abstractmethod
    async def update(self, profile: FitnessProfile) -> FitnessProfile:
        ...

    @abstractmethod
    async def find_partners(
        self,
        community_id: int,
        exclude_user_id: int,
        workout_types: list[WorkoutType] | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[FitnessProfile]:
        ...
