from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.venue_request import VenueRequest
from app.schemas.venue_request import VenueRequestIn
from app.services.email import notify_venue_request

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