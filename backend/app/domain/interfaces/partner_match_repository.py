from abc import ABC, abstractmethod

from app.domain.entities.partner_match import PartnerMatch


class PartnerMatchRepository(ABC):
    @abstractmethod
    async def get_by_id(self, match_id: int) -> PartnerMatch | None:
        ...

    @abstractmethod
    async def create(self, match: PartnerMatch) -> PartnerMatch:
        ...

    @abstractmethod
    async def update(self, match: PartnerMatch) -> PartnerMatch:
        ...

    @abstractmethod
    async def list_for_user(self, user_id: int) -> list[PartnerMatch]:
        ...

    @abstractmethod
    async def find_existing(
        self, requester_id: int, recipient_id: int
    ) -> PartnerMatch | None:
        ...
