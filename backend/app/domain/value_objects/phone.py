import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self) -> None:
        cleaned = re.sub(r"[\s\-()]", "", self.value)
        if not re.match(r"^\+?[0-9]{10,15}$", cleaned):
            raise ValueError(f"Invalid phone number: {self.value}")

    def __str__(self) -> str:
        return self.value
