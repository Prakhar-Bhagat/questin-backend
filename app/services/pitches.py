from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pitch import Pitch
from app.schemas.pitch import PitchIn
from app.services.email import notify_pitch

async def create_pitch(data: PitchIn, db: AsyncSession) -> Pitch:
    record = Pitch(**data.model_dump(), status="pending")
    db.add(record)
    await db.commit()
    await db.refresh(record)
    await notify_pitch(
        data.community_name, data.organizer_name,
        data.email, data.category, data.description
    )
    return record