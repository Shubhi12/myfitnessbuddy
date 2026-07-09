from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError("End time must be after start time")

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)
