from abc import ABC, abstractmethod

from app.domain.entities.amenity import Amenity


class AmenityRepository(ABC):
    @abstractmethod
    async def get_by_id(self, amenity_id: int) -> Amenity | None:
        ...

    @abstractmethod
    async def create(self, amenity: Amenity) -> Amenity:
        ...

    @abstractmethod
    async def update(self, amenity: Amenity) -> Amenity:
        ...

    @abstractmethod
    async def list_by_community(
        self, community_id: int, skip: int = 0, limit: int = 50
    ) -> list[Amenity]:
        ...
