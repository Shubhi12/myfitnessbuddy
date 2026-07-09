from fastapi import APIRouter

from app.presentation.api.v1 import (
    amenities,
    auth,
    bookings,
    communities,
    fitness_profiles,
    notifications,
    partners,
    users,
)
from app.presentation.api.v1.admin import users as admin_users

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(communities.router)
api_v1_router.include_router(fitness_profiles.router)
api_v1_router.include_router(partners.router)
api_v1_router.include_router(amenities.router)
api_v1_router.include_router(bookings.router)
api_v1_router.include_router(notifications.router)
api_v1_router.include_router(admin_users.router)
