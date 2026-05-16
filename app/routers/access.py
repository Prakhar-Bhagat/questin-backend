from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.access_request import AccessRequestIn, AccessRequestOut, AccessRequestStatusUpdate
from app.services import access as svc
from app.auth import require_admin
from fastapi import Request
from app.limiter import limiter
from sqlalchemy import func
from app.models.waitlist import Waitlist
from app.models.pitch import Pitch
from app.models.venue_request import VenueRequest
from app.services.email import send_login_link
router = APIRouter()

@router.post("/", response_model=AccessRequestOut, status_code=201)
@limiter.limit("3/minute")
async def submit_access_request(request: Request, data: AccessRequestIn, db: AsyncSession = Depends(get_db)):
    return await svc.create_access_request(data, db)

@router.get("/", response_model=list[AccessRequestOut], dependencies=[Depends(require_admin)])
async def list_requests(db: AsyncSession = Depends(get_db)):
    return await svc.list_access_requests(db)

@router.patch("/{id}/status", response_model=AccessRequestStatusUpdate, dependencies=[Depends(require_admin)])
async def update_status(
    id: int,
    status: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    if status not in ("pending", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status value")
    return await svc.update_access_request_status(id, status, db)

@router.get("/stats", dependencies=[Depends(require_admin)])
async def get_stats(db: AsyncSession = Depends(get_db)):
    async def count(model, **filters):
        q = select(func.count()).select_from(model)
        for col, val in filters.items():
            q = q.where(getattr(model, col) == val)
        return (await db.execute(q)).scalar()

    return {
        "access_requests": {
            "total":    await count(AccessRequest),
            "pending":  await count(AccessRequest, status="pending"),
            "approved": await count(AccessRequest, status="approved"),
            "rejected": await count(AccessRequest, status="rejected"),
        },
        "venue_requests": {
            "total":   await count(VenueRequest),
            "pending": await count(VenueRequest, status="pending"),
        },
        "pitches": {
            "total":   await count(Pitch),
            "pending": await count(Pitch, status="pending"),
        },
        "waitlist": {
            "total": await count(Waitlist),
        },
    }

@router.post("/login")
async def request_login(email: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AccessRequest).where(
            AccessRequest.email == email,
            AccessRequest.status == "approved"
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        # Don't reveal whether email exists or not
        return {"message": "If that email is approved, a login link is on its way."}
    token = create_access_token(record.email)
    await send_login_link(record.email, record.name, token)
    return {"message": "If that email is approved, a login link is on its way."}