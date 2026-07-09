from dataclasses import dataclass

from app.application.dto.user_dto import UserListQueryDTO, UserUpdateDTO
from app.core.exceptions.base import NotFoundError
from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository


@dataclass
class UserService:
    user_repo: UserRepository

    async def get_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    async def list_by_community(self, query: UserListQueryDTO) -> list[User]:
        return await self.user_repo.list_by_community(
            query.community_id, query.skip, query.limit
        )

    async def update_profile(self, user_id: int, dto: UserUpdateDTO) -> User:
        user = await self.get_by_id(user_id)
        if dto.full_name:
            user.full_name = dto.full_name
        if dto.phone is not None:
            user.phone = dto.phone
        return await self.user_repo.update(user)
