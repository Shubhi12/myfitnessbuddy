from dataclasses import dataclass

from app.application.dto.amenity_dto import AmenityCreateDTO
from app.application.interfaces.cache_service import CacheService
from app.core.exceptions.base import NotFoundError
from app.domain.entities.amenity import Amenity
from app.domain.interfaces.amenity_repository import AmenityRepository


@dataclass
class AmenityService:
    amenity_repo: AmenityRepository
    cache: CacheService

    async def get_by_id(self, amenity_id: int) -> Amenity:
        cache_key = f"amenity:{amenity_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return Amenity(**cached)

        amenity = await self.amenity_repo.get_by_id(amenity_id)
        if not amenity:
            raise NotFoundError("Amenity", amenity_id)

        await self.cache.set(cache_key, amenity.__dict__, ttl_seconds=600)
        return amenity

    async def list_by_community(self, community_id: int) -> list[Amenity]:
        return await self.amenity_repo.list_by_community(community_id)

    async def create(self, dto: AmenityCreateDTO) -> Amenity:
        amenity = Amenity(
            id=None,
            community_id=dto.community_id,
            name=dto.name,
            amenity_type=dto.amenity_type,
            description=dto.description,
            capacity=dto.capacity,
            open_time=dto.open_time,
            close_time=dto.close_time,
            slot_duration_minutes=dto.slot_duration_minutes,
        )
        created = await self.amenity_repo.create(amenity)
        await self.cache.invalidate_pattern(f"amenities:community:{dto.community_id}*")
        return created
