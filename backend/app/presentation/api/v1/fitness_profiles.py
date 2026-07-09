from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.di.container import ServiceContainer
from app.domain.entities.fitness_profile import FitnessProfile
from app.domain.entities.user import User
from app.domain.enums.workout_type import WorkoutType
from app.presentation.api.deps import get_current_user, get_services
from app.presentation.schemas.fitness_profile import (
    FitnessProfileCreateRequest,
    FitnessProfileResponse,
)

router = APIRouter(prefix="/fitness-profiles", tags=["Fitness Profiles"])


@router.get("/me", response_model=FitnessProfileResponse)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> FitnessProfile:
    return await services.fitness_profile.get_by_user_id(current_user.id)  # type: ignore[arg-type]


@router.put("/me", response_model=FitnessProfileResponse)
async def upsert_my_profile(
    body: FitnessProfileCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> FitnessProfile:
    return await services.fitness_profile.create_or_update(
        user_id=current_user.id,  # type: ignore[arg-type]
        fitness_level=body.fitness_level,
        preferred_workouts=body.preferred_workouts,
        bio=body.bio,
        preferred_time_start=body.preferred_time_start,
        preferred_time_end=body.preferred_time_end,
        is_seeking_partner=body.is_seeking_partner,
    )


@router.get("/partners", response_model=list[FitnessProfileResponse])
async def discover_partners(
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
    workout_type: WorkoutType | None = None,
) -> list[FitnessProfile]:
    workout_types = [workout_type] if workout_type else None
    return await services.fitness_profile.find_partners(
        community_id=current_user.community_id,
        exclude_user_id=current_user.id,  # type: ignore[arg-type]
        workout_types=workout_types,
    )
