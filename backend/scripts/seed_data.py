#!/usr/bin/env python3
"""Seed sample amenities for gated communities."""

import asyncio
import sys
from datetime import time
from pathlib import Path

from sqlalchemy import select

# Allow running as `python scripts/seed_data.py` from /app in Docker
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.enums.amenity_type import AmenityType
from app.infrastructure.database.models.amenity_model import AmenityModel
from app.infrastructure.database.models.community_model import CommunityModel
from app.infrastructure.database.session import AsyncSessionLocal

COMMUNITY_IDS = [3, 4]

AMENITIES: list[tuple[str, AmenityType, str, int]] = [
    ("Rain forest", AmenityType.GYM, "Fully equipped community gym", 25),
    ("Oasis", AmenityType.BADMINTON_COURT, "Indoor badminton courts with professional flooring", 4),
    ("Green forest", AmenityType.TABLE_TENNIS, "Table tennis room with multiple tables", 4),
    ("Swimming Pool", AmenityType.POOL, "Community swimming pool with lane markers", 20),
]

OPEN_TIME = time(6, 0)
CLOSE_TIME = time(22, 0)
SLOT_DURATION_MINUTES = 60


async def seed_amenities() -> None:
    async with AsyncSessionLocal() as session:
        created_count = 0
        skipped_count = 0

        for community_id in COMMUNITY_IDS:
            community = await session.get(CommunityModel, community_id)
            if community is None:
                print(f"Warning: community id={community_id} not found, skipping")
                continue

            print(f"Seeding amenities for community id={community_id} ({community.name})")

            for name, amenity_type, description, capacity in AMENITIES:
                existing = await session.scalar(
                    select(AmenityModel).where(
                        AmenityModel.community_id == community_id,
                        AmenityModel.name == name,
                    )
                )
                if existing:
                    print(f"  - Skip '{name}' (already exists)")
                    skipped_count += 1
                    continue

                session.add(
                    AmenityModel(
                        community_id=community_id,
                        name=name,
                        amenity_type=amenity_type.value,
                        description=description,
                        capacity=capacity,
                        open_time=OPEN_TIME,
                        close_time=CLOSE_TIME,
                        slot_duration_minutes=SLOT_DURATION_MINUTES,
                        is_active=True,
                    )
                )
                print(f"  + Created '{name}' ({amenity_type.value})")
                created_count += 1

        await session.commit()
        print(f"\nDone. Created {created_count} amenities, skipped {skipped_count}.")


def main() -> None:
    asyncio.run(seed_amenities())


if __name__ == "__main__":
    main()
