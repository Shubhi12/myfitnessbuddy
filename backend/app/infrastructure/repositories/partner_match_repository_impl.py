from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.partner_match import PartnerMatch
from app.domain.enums.match_status import MatchStatus
from app.domain.interfaces.partner_match_repository import PartnerMatchRepository
from app.infrastructure.database.models.partner_match_model import PartnerMatchModel


def _to_entity(model: PartnerMatchModel) -> PartnerMatch:
    return PartnerMatch(
        id=model.id,
        requester_id=model.requester_id,
        recipient_id=model.recipient_id,
        status=MatchStatus(model.status),
        message=model.message,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class PartnerMatchRepositoryImpl(PartnerMatchRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, match_id: int) -> PartnerMatch | None:
        result = await self._session.get(PartnerMatchModel, match_id)
        return _to_entity(result) if result else None

    async def create(self, match: PartnerMatch) -> PartnerMatch:
        model = PartnerMatchModel(
            requester_id=match.requester_id,
            recipient_id=match.recipient_id,
            status=match.status.value,
            message=match.message,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, match: PartnerMatch) -> PartnerMatch:
        model = await self._session.get(PartnerMatchModel, match.id)
        if not model:
            raise ValueError(f"Match {match.id} not found")
        model.status = match.status.value
        model.message = match.message
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_for_user(self, user_id: int) -> list[PartnerMatch]:
        stmt = select(PartnerMatchModel).where(
            or_(
                PartnerMatchModel.requester_id == user_id,
                PartnerMatchModel.recipient_id == user_id,
            )
        )
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]

    async def find_existing(
        self, requester_id: int, recipient_id: int
    ) -> PartnerMatch | None:
        stmt = select(PartnerMatchModel).where(
            or_(
                and_(
                    PartnerMatchModel.requester_id == requester_id,
                    PartnerMatchModel.recipient_id == recipient_id,
                ),
                and_(
                    PartnerMatchModel.requester_id == recipient_id,
                    PartnerMatchModel.recipient_id == requester_id,
                ),
            )
        )
        result = await self._session.scalar(stmt)
        return _to_entity(result) if result else None
