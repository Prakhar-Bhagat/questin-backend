from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.venue_request import VenueRequestIn, VenueRequestOut
from app.services import venue_requests as svc
from app.auth import require_admin, require_catalogue_access

router = APIRouter()

@router.patch("/{request_id}/status", response_model=VenueRequestOut, dependencies=[Depends(require_admin)])
async def update_venue_request_status(
    request_id: int,
    status: str,
    db: AsyncSession = Depends(get_db)
):
    # Pass it to your service layer
    return await svc.update_venue_status(request_id, status, db)

@router.post("/", response_model=VenueRequestOut, status_code=201)
async def submit_venue_request(
    data: VenueRequestIn,
    db: AsyncSession = Depends(get_db),
    email: str = Depends(require_catalogue_access)  # must be an approved user
):
    return await svc.create_venue_request(data, db)

@router.post("/", response_model=VenueRequestOut, status_code=201)
async def submit_venue_request(
    data: VenueRequestIn,
    db: AsyncSession = Depends(get_db),
    email: str = Depends(require_catalogue_access)  
):
    return await svc.create_venue_request(data, email, db)

@router.get("/", response_model=list[VenueRequestOut], dependencies=[Depends(require_admin)])
async def list_venue_requests(db: AsyncSession = Depends(get_db)):
    return await svc.list_venue_requests(db)
# force redeploy