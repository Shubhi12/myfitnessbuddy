from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.cache_service import CacheService
from app.application.services.amenity_service import AmenityService
from app.application.services.auth_service import AuthService
from app.application.services.booking_service import BookingService
from app.application.services.community_service import CommunityService
from app.application.services.fitness_profile_service import FitnessProfileService
from app.application.services.notification_service import NotificationService
from app.application.services.partner_matching_service import PartnerMatchingService
from app.application.services.user_service import UserService
from app.infrastructure.cache.redis_cache_service import RedisCacheService
from app.infrastructure.repositories.amenity_repository_impl import AmenityRepositoryImpl
from app.infrastructure.repositories.booking_repository_impl import BookingRepositoryImpl
from app.infrastructure.repositories.community_repository_impl import CommunityRepositoryImpl
from app.infrastructure.repositories.fitness_profile_repository_impl import (
    FitnessProfileRepositoryImpl,
)
from app.infrastructure.repositories.notification_repository_impl import (
    NotificationRepositoryImpl,
)
from app.infrastructure.repositories.partner_match_repository_impl import (
    PartnerMatchRepositoryImpl,
)
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl


@dataclass
class ServiceContainer:
    auth: AuthService
    user: UserService
    community: CommunityService
    fitness_profile: FitnessProfileService
    partner_matching: PartnerMatchingService
    amenity: AmenityService
    booking: BookingService
    notification: NotificationService


def build_services(session: AsyncSession, cache: CacheService | None = None) -> ServiceContainer:
    cache_service = cache or RedisCacheService()

    user_repo = UserRepositoryImpl(session)
    community_repo = CommunityRepositoryImpl(session)
    profile_repo = FitnessProfileRepositoryImpl(session)
    match_repo = PartnerMatchRepositoryImpl(session)
    amenity_repo = AmenityRepositoryImpl(session)
    booking_repo = BookingRepositoryImpl(session)
    notification_repo = NotificationRepositoryImpl(session)

    return ServiceContainer(
        auth=AuthService(user_repo, community_repo),
        user=UserService(user_repo),
        community=CommunityService(community_repo),
        fitness_profile=FitnessProfileService(profile_repo),
        partner_matching=PartnerMatchingService(match_repo, profile_repo, user_repo),
        amenity=AmenityService(amenity_repo, cache_service),
        booking=BookingService(booking_repo, amenity_repo, notification_repo),
        notification=NotificationService(notification_repo),
    )
