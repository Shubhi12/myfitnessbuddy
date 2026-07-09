from dataclasses import dataclass
from datetime import time

from app.core.exceptions.base import ConflictError, NotFoundError
from app.domain.entities.fitness_profile import FitnessProfile
from app.domain.enums.fitness_level import FitnessLevel
from app.domain.enums.workout_type import WorkoutType
from app.domain.interfaces.fitness_profile_repository import FitnessProfileRepository


@dataclass
class FitnessProfileService:
    profile_repo: FitnessProfileRepository

    async def get_by_user_id(self, user_id: int) -> FitnessProfile:
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("FitnessProfile", user_id)
        return profile

    async def create_or_update(
        self,
        user_id: int,
        fitness_level: FitnessLevel,
        preferred_workouts: list[WorkoutType],
        bio: str | None = None,
        preferred_time_start: time | None = None,
        preferred_time_end: time | None = None,
        is_seeking_partner: bool = True,
    ) -> FitnessProfile:
        existing = await self.profile_repo.get_by_user_id(user_id)
        if existing:
            existing.fitness_level = fitness_level
            existing.preferred_workouts = preferred_workouts
            existing.bio = bio
            existing.preferred_time_start = preferred_time_start
            existing.preferred_time_end = preferred_time_end
            existing.is_seeking_partner = is_seeking_partner
            return await self.profile_repo.update(existing)

        profile = FitnessProfile(
            id=None,
            user_id=user_id,
            fitness_level=fitness_level,
            preferred_workouts=preferred_workouts,
            bio=bio,
            preferred_time_start=preferred_time_start,
            preferred_time_end=preferred_time_end,
            is_seeking_partner=is_seeking_partner,
        )
        return await self.profile_repo.create(profile)

    async def find_partners(
        self,
        community_id: int,
        exclude_user_id: int,
        workout_types: list[WorkoutType] | None = None,
    ) -> list[FitnessProfile]:
        return await self.profile_repo.find_partners(
            community_id, exclude_user_id, workout_types
        )
