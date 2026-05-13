from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.waitlist import Waitlist
from app.schemas.waitlist import WaitlistIn
from app.services.email import notify_waitlist

async def add_to_waitlist(data: WaitlistIn, db: AsyncSession) -> Waitlist:
    record = Waitlist(email=data.email)
    db.add(record)
    try:
        await db.commit()
        await db.refresh(record)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already on waitlist")
    await notify_waitlist(data.email)
    return record