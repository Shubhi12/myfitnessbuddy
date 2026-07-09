from dataclasses import dataclass

from app.core.exceptions.base import NotFoundError
from app.domain.entities.community import Community
from app.domain.interfaces.community_repository import CommunityRepository


@dataclass
class CommunityService:
    community_repo: CommunityRepository

    async def get_by_id(self, community_id: int) -> Community:
        community = await self.community_repo.get_by_id(community_id)
        if not community:
            raise NotFoundError("Community", community_id)
        return community

    async def list_all(self, skip: int = 0, limit: int = 50) -> list[Community]:
        return await self.community_repo.list_all(skip, limit)

    async def create(self, community: Community) -> Community:
        return await self.community_repo.create(community)
