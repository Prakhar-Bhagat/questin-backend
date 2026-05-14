from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.venue_request import VenueRequest
from app.schemas.venue_request import VenueRequestIn
from app.services.email import notify_venue_request, notify_venue_status_update

async def update_venue_status(request_id: int, status: str, db: AsyncSession) -> VenueRequest:
    # 1. Validate the status
    valid_statuses = ["pending", "approved", "rejected"]
    if status not in valid_statuses:
        raise HTTPException(status_code=422, detail=f"Status must be one of {valid_statuses}")

    # 2. Fetch the existing request
    result = await db.execute(select(VenueRequest).where(VenueRequest.id == request_id))
    db_req = result.scalar_one_or_none()

    if not db_req:
        raise HTTPException(status_code=404, detail="Venue request not found")

    # Store old status so we only send an email if the status ACTUALLY changed
    old_status = db_req.status

    # 3. Update, commit, and return
    db_req.status = status
    await db.commit()
    await db.refresh(db_req)
    
    # 4. Trigger the email notification
    if old_status != status and status in ["approved", "rejected"]:
        await notify_venue_status_update(
            to_email=db_req.email, 
            poc_name=db_req.poc_name,
            new_status=status,
            community_id=db_req.community_id
        )
    
    return db_req


async def create_venue_request(data: VenueRequestIn, email: str, db: AsyncSession) -> VenueRequest:
    record = VenueRequest(
        community_id=data.community_id,
        email=email,
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