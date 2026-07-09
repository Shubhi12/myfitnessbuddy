from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        full_name=model.full_name,
        phone=model.phone,
        role=UserRole(model.role),
        community_id=model.community_id,
        is_active=model.is_active,
        hashed_password=model.hashed_password,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.get(UserModel, user_id)
        return _to_entity(result) if result else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.scalar(stmt)
        return _to_entity(result) if result else None

    async def create(self, user: User) -> User:
        model = UserModel(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            phone=user.phone,
            role=user.role.value,
            community_id=user.community_id,
            is_active=user.is_active,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, user: User) -> User:
        model = await self._session.get(UserModel, user.id)
        if not model:
            raise ValueError(f"User {user.id} not found")
        model.full_name = user.full_name
        model.phone = user.phone
        model.is_active = user.is_active
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_by_community(
        self, community_id: int, skip: int = 0, limit: int = 50
    ) -> list[User]:
        stmt = (
            select(UserModel)
            .where(UserModel.community_id == community_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]
