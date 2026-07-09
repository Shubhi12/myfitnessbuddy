from dataclasses import dataclass

from app.application.dto.auth_dto import AdminRegisterDTO, AuthTokensDTO, LoginDTO, RegisterDTO
from app.core.config.settings import get_settings
from app.core.exceptions.base import ConflictError, ForbiddenError, UnauthorizedError
from app.core.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.domain.entities.community import Community
from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole
from app.domain.interfaces.community_repository import CommunityRepository
from app.domain.interfaces.user_repository import UserRepository


@dataclass
class AuthService:
    user_repo: UserRepository
    community_repo: CommunityRepository

    async def register(self, dto: RegisterDTO) -> AuthTokensDTO:
        existing = await self.user_repo.get_by_email(dto.email)
        if existing:
            raise ConflictError("Email already registered")

        user = User(
            id=None,
            email=dto.email,
            full_name=dto.full_name,
            phone=dto.phone,
            role=UserRole.RESIDENT,
            community_id=dto.community_id,
            hashed_password=hash_password(dto.password),
        )
        created = await self.user_repo.create(user)
        return self._build_tokens(created)

    async def register_admin(self, dto: AdminRegisterDTO) -> AuthTokensDTO:
        settings = get_settings()
        if not settings.allow_admin_signup:
            raise ForbiddenError("Admin signup is currently disabled")

        existing = await self.user_repo.get_by_email(dto.email)
        if existing:
            raise ConflictError("Email already registered")

        community = Community(
            id=None,
            name=dto.community_name,
            address=dto.community_address,
            city=dto.community_city,
            pincode=dto.community_pincode,
        )
        created_community = await self.community_repo.create(community)

        user = User(
            id=None,
            email=dto.email,
            full_name=dto.full_name,
            phone=dto.phone,
            role=UserRole.ADMIN,
            community_id=created_community.id,  # type: ignore[arg-type]
            hashed_password=hash_password(dto.password),
        )
        created = await self.user_repo.create(user)
        return self._build_tokens(created)

    async def login(self, dto: LoginDTO) -> AuthTokensDTO:
        user = await self.user_repo.get_by_email(dto.email)
        if not user or not verify_password(dto.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")
        return self._build_tokens(user)

    async def login_admin(self, dto: LoginDTO) -> AuthTokensDTO:
        user = await self.user_repo.get_by_email(dto.email)
        if not user or not verify_password(dto.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")
        if user.role != UserRole.ADMIN:
            raise ForbiddenError("Admin access required")
        return self._build_tokens(user)

    async def refresh_token(self, refresh_token: str) -> AuthTokensDTO:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")
        user = await self.user_repo.get_by_id(int(payload["sub"]))
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        return self._build_tokens(user)

    def _build_tokens(self, user: User) -> AuthTokensDTO:
        claims = {"role": user.role.value, "community_id": user.community_id}
        return AuthTokensDTO(
            access_token=create_access_token(str(user.id), claims),
            refresh_token=create_refresh_token(str(user.id)),
            token_type="bearer",
        )
