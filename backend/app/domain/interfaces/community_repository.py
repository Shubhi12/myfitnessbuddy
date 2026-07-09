from abc import ABC, abstractmethod

from app.domain.entities.community import Community


class CommunityRepository(ABC):
    @abstractmethod
    async def get_by_id(self, community_id: int) -> Community | None:
        ...

    @abstractmethod
    async def create(self, community: Community) -> Community:
        ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 50) -> list[Community]:
        ...

    @abstractmethod
    async def update(self, community: Community) -> Community:
        ...
