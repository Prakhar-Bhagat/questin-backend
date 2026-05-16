from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.community import Community
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

    # 3. Fetch the community for contact details
    comm_result = await db.execute(select(Community).where(Community.id == db_req.community_id))
    community = comm_result.scalar_one_or_none()

    # 4. Update, commit, and refresh
    db_req.status = status
    await db.commit()
    await db.refresh(db_req)
    
    # 5. Trigger the expanded email notification
    if old_status != status and status in ["approved", "rejected"]:
        await notify_venue_status_update(
            to_email=db_req.email,  # Using .email to match your original schema
            poc_name=db_req.poc_name,
            new_status=status,
            community_name=community.name if community else f"#{db_req.community_id}",
            community_contact_name=community.contact_name if community else None,
            community_contact_email=community.contact_email if community else None,
            community_contact_phone=community.contact_phone if community else None,
        )
    
    return db_req


async def create_venue_request(data: VenueRequestIn, email: str, db: AsyncSession) -> VenueRequest:
    existing = await db.execute(
        select(VenueRequest).where(
            VenueRequest.community_id == data.community_id,
            VenueRequest.email == email
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="You've already requested this community.")
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