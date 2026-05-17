from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.venue_request import VenueRequestIn, VenueRequestOut
from app.services import venue_requests as svc
from app.auth import require_approved_venue, require_admin

router = APIRouter()

@router.post("/", response_model=VenueRequestOut, status_code=201)
async def submit_venue_request(
    data: VenueRequestIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_approved_venue)
):
    return await svc.create_venue_request(data, current_user.email, db)

@router.get("/", response_model=list[VenueRequestOut], dependencies=[Depends(require_admin)])
async def list_venue_requests(db: AsyncSession = Depends(get_db)):
    return await svc.list_venue_requests(db)

@router.patch("/{request_id}/status", response_model=VenueRequestOut, dependencies=[Depends(require_admin)])
async def update_venue_request_status(
    request_id: int,
    status: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    if status not in ("pending", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status")
    return await svc.update_venue_status(request_id, status, db)