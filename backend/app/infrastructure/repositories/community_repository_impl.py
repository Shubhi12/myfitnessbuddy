from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.community import Community
from app.domain.interfaces.community_repository import CommunityRepository
from app.infrastructure.database.models.community_model import CommunityModel


def _to_entity(model: CommunityModel) -> Community:
    return Community(
        id=model.id,
        name=model.name,
        address=model.address,
        city=model.city,
        pincode=model.pincode,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class CommunityRepositoryImpl(CommunityRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, community_id: int) -> Community | None:
        result = await self._session.get(CommunityModel, community_id)
        return _to_entity(result) if result else None

    async def create(self, community: Community) -> Community:
        model = CommunityModel(
            name=community.name,
            address=community.address,
            city=community.city,
            pincode=community.pincode,
            is_active=community.is_active,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_all(self, skip: int = 0, limit: int = 50) -> list[Community]:
        stmt = select(CommunityModel).offset(skip).limit(limit)
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]

    async def update(self, community: Community) -> Community:
        model = await self._session.get(CommunityModel, community.id)
        if not model:
            raise ValueError(f"Community {community.id} not found")
        model.name = community.name
        model.address = community.address
        model.city = community.city
        model.pincode = community.pincode
        model.is_active = community.is_active
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)
