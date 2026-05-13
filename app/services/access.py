from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.access_request import AccessRequest
from app.schemas.access_request import AccessRequestIn
from app.auth import create_access_token
from app.services.email import (
    notify_access_request,
    send_access_approved,
    send_access_rejected
)

async def create_access_request(data: AccessRequestIn, db: AsyncSession) -> AccessRequest:
    record = AccessRequest(
        name=data.name,
        email=data.email,
        about=data.about,
        user_type=data.user_type,
        status="pending"
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    await notify_access_request(data.name, data.email, data.about, data.user_type)
    return record

async def list_access_requests(db: AsyncSession) -> list[AccessRequest]:
    result = await db.execute(
        select(AccessRequest).order_by(AccessRequest.created_at.desc())
    )
    return result.scalars().all()

async def update_access_request_status(id: int, status: str, db: AsyncSession) -> dict:
    result = await db.execute(select(AccessRequest).where(AccessRequest.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Request not found")
    record.status = status
    await db.commit()
    await db.refresh(record)

    token = None
    if status == "approved":
        token = create_access_token(record.email)
        await send_access_approved(record.email, record.name, token)
    elif status == "rejected":
        await send_access_rejected(record.email, record.name)

    return {"request": record, "token": token}