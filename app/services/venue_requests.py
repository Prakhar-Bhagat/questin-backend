from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.venue_request import VenueRequest
from app.schemas.venue_request import VenueRequestIn
from app.services.email import notify_venue_request
from fastapi import HTTPException

async def update_venue_status(request_id: int, status: str, db: AsyncSession):
    # 1. Validate the status
    valid_statuses = ["pending", "approved", "rejected"]
    if status not in valid_statuses:
        raise HTTPException(status_code=422, detail=f"Status must be one of {valid_statuses}")

    # 2. Fetch the existing request
    result = await db.execute(select(VenueRequest).where(VenueRequest.id == request_id))
    db_req = result.scalar_one_or_none()

    if not db_req:
        raise HTTPException(status_code=404, detail="Venue request not found")

    # 3. Update, commit, and return
    db_req.status = status
    await db.commit()
    await db.refresh(db_req)
    
    return db_req

async def create_venue_request(data: VenueRequestIn, db: AsyncSession) -> VenueRequest:
    record = VenueRequest(
        community_id=data.community_id,
        poc_name=data.poc,
        phone=data.phone,
        preferred_dates=data.dates,
        capacity=data.capacity,
        revenue_model=data.revenue,
        notes=data.notes,
        status="pending"
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    await notify_venue_request(
        data.poc, data.phone, data.community_id,
        data.dates, data.capacity, data.revenue, data.notes
    )
    return record

async def list_venue_requests(db: AsyncSession) -> list[VenueRequest]:
    result = await db.execute(select(VenueRequest).order_by(VenueRequest.created_at.desc()))
    return result.scalars().all()