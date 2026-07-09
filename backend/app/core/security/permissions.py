from app.domain.enums.user_role import UserRole

ROLE_PERMISSIONS: dict[UserRole, set[str]] = {
    UserRole.RESIDENT: {
        "profile:read",
        "profile:write",
        "partners:read",
        "partners:write",
        "amenities:read",
        "bookings:read",
        "bookings:write",
    },
    UserRole.ADMIN: {
        "profile:read",
        "profile:write",
        "partners:read",
        "partners:write",
        "amenities:read",
        "amenities:write",
        "bookings:read",
        "bookings:write",
        "users:read",
        "users:write",
        "communities:read",
        "communities:write",
        "admin:dashboard",
    },
}


def has_permission(role: UserRole, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())
