from dataclasses import dataclass

from app.application.dto.partner_dto import PartnerRequestDTO, PartnerRespondDTO
from app.core.exceptions.base import ConflictError, ForbiddenError, NotFoundError
from app.domain.entities.partner_match import PartnerMatch
from app.domain.enums.match_status import MatchStatus
from app.domain.interfaces.fitness_profile_repository import FitnessProfileRepository
from app.domain.interfaces.partner_match_repository import PartnerMatchRepository
from app.domain.interfaces.user_repository import UserRepository


@dataclass
class PartnerMatchingService:
    match_repo: PartnerMatchRepository
    profile_repo: FitnessProfileRepository
    user_repo: UserRepository

    async def send_request(self, dto: PartnerRequestDTO) -> PartnerMatch:
        if dto.requester_id == dto.recipient_id:
            raise ConflictError("Cannot send partner request to yourself")

        recipient = await self.user_repo.get_by_id(dto.recipient_id)
        if not recipient:
            raise NotFoundError("User", dto.recipient_id)

        requester = await self.user_repo.get_by_id(dto.requester_id)
        if not requester or requester.community_id != recipient.community_id:
            raise ForbiddenError("Users must be in the same community")

        existing = await self.match_repo.find_existing(dto.requester_id, dto.recipient_id)
        if existing and existing.status in (MatchStatus.PENDING, MatchStatus.ACCEPTED):
            raise ConflictError("Partner request already exists")

        match = PartnerMatch(
            id=None,
            requester_id=dto.requester_id,
            recipient_id=dto.recipient_id,
            status=MatchStatus.PENDING,
            message=dto.message,
        )
        return await self.match_repo.create(match)

    async def respond_to_request(self, dto: PartnerRespondDTO) -> PartnerMatch:
        match = await self.match_repo.get_by_id(dto.match_id)
        if not match:
            raise NotFoundError("PartnerMatch", dto.match_id)
        if match.recipient_id != dto.user_id:
            raise ForbiddenError("Only the recipient can respond to this request")
        if match.status != MatchStatus.PENDING:
            raise ConflictError("Request is no longer pending")

        match.status = MatchStatus.ACCEPTED if dto.accept else MatchStatus.REJECTED
        return await self.match_repo.update(match)

    async def list_matches(self, user_id: int) -> list[PartnerMatch]:
        return await self.match_repo.list_for_user(user_id)
