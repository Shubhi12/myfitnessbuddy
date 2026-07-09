from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.fitness_profile import FitnessProfile
from app.domain.enums.fitness_level import FitnessLevel
from app.domain.enums.workout_type import WorkoutType
from app.domain.interfaces.fitness_profile_repository import FitnessProfileRepository
from app.infrastructure.database.models.fitness_profile_model import FitnessProfileModel
from app.infrastructure.database.models.user_model import UserModel


def _to_entity(model: FitnessProfileModel) -> FitnessProfile:
    return FitnessProfile(
        id=model.id,
        user_id=model.user_id,
        fitness_level=FitnessLevel(model.fitness_level),
        preferred_workouts=[WorkoutType(w) for w in model.workouts_list],
        bio=model.bio,
        preferred_time_start=model.preferred_time_start,
        preferred_time_end=model.preferred_time_end,
        is_seeking_partner=model.is_seeking_partner,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class FitnessProfileRepositoryImpl(FitnessProfileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: int) -> FitnessProfile | None:
        stmt = select(FitnessProfileModel).where(FitnessProfileModel.user_id == user_id)
        result = await self._session.scalar(stmt)
        return _to_entity(result) if result else None

    async def create(self, profile: FitnessProfile) -> FitnessProfile:
        model = FitnessProfileModel(
            user_id=profile.user_id,
            fitness_level=profile.fitness_level.value,
            bio=profile.bio,
            preferred_time_start=profile.preferred_time_start,
            preferred_time_end=profile.preferred_time_end,
            is_seeking_partner=profile.is_seeking_partner,
        )
        model.workouts_list = [w.value for w in profile.preferred_workouts]
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, profile: FitnessProfile) -> FitnessProfile:
        model = await self._session.get(FitnessProfileModel, profile.id)
        if not model:
            raise ValueError(f"Profile {profile.id} not found")
        model.fitness_level = profile.fitness_level.value
        model.workouts_list = [w.value for w in profile.preferred_workouts]
        model.bio = profile.bio
        model.preferred_time_start = profile.preferred_time_start
        model.preferred_time_end = profile.preferred_time_end
        model.is_seeking_partner = profile.is_seeking_partner
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_partners(
        self,
        community_id: int,
        exclude_user_id: int,
        workout_types: list[WorkoutType] | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[FitnessProfile]:
        stmt = (
            select(FitnessProfileModel)
            .join(UserModel, FitnessProfileModel.user_id == UserModel.id)
            .where(
                UserModel.community_id == community_id,
                FitnessProfileModel.user_id != exclude_user_id,
                FitnessProfileModel.is_seeking_partner.is_(True),
                UserModel.is_active.is_(True),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        profiles = [_to_entity(m) for m in result.all()]
        if workout_types:
            workout_values = {w.value for w in workout_types}
            profiles = [
                p
                for p in profiles
                if any(w.value in workout_values for w in p.preferred_workouts)
            ]
        return profiles
