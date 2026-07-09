from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.amenity import Amenity
from app.domain.enums.amenity_type import AmenityType
from app.domain.interfaces.amenity_repository import AmenityRepository
from app.infrastructure.database.models.amenity_model import AmenityModel


def _to_entity(model: AmenityModel) -> Amenity:
    return Amenity(
        id=model.id,
        community_id=model.community_id,
        name=model.name,
        amenity_type=AmenityType(model.amenity_type),
        description=model.description,
        capacity=model.capacity,
        open_time=model.open_time,
        close_time=model.close_time,
        slot_duration_minutes=model.slot_duration_minutes,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class AmenityRepositoryImpl(AmenityRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, amenity_id: int) -> Amenity | None:
        result = await self._session.get(AmenityModel, amenity_id)
        return _to_entity(result) if result else None

    async def create(self, amenity: Amenity) -> Amenity:
        model = AmenityModel(
            community_id=amenity.community_id,
            name=amenity.name,
            amenity_type=amenity.amenity_type.value,
            description=amenity.description,
            capacity=amenity.capacity,
            open_time=amenity.open_time,
            close_time=amenity.close_time,
            slot_duration_minutes=amenity.slot_duration_minutes,
            is_active=amenity.is_active,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, amenity: Amenity) -> Amenity:
        model = await self._session.get(AmenityModel, amenity.id)
        if not model:
            raise ValueError(f"Amenity {amenity.id} not found")
        model.name = amenity.name
        model.description = amenity.description
        model.capacity = amenity.capacity
        model.open_time = amenity.open_time
        model.close_time = amenity.close_time
        model.slot_duration_minutes = amenity.slot_duration_minutes
        model.is_active = amenity.is_active
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_by_community(
        self, community_id: int, skip: int = 0, limit: int = 50
    ) -> list[Amenity]:
        stmt = (
            select(AmenityModel)
            .where(AmenityModel.community_id == community_id, AmenityModel.is_active.is_(True))
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]
