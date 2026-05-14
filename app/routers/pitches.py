from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.pitch import PitchIn, PitchOut
from app.services import pitches as svc
from app.models.pitch import Pitch
from app.auth import require_admin   
from app.limiter import limiter

router = APIRouter()

# --- PUBLIC ROUTE ---
@router.post("/", response_model=PitchOut, status_code=201)
@limiter.limit("3/minute")
async def submit_pitch(request: Request, data: PitchIn, db: AsyncSession = Depends(get_db)):
    return await svc.create_pitch(data, db)

# --- ADMIN ROUTES (Needed for the Dashboard) ---

@router.get("/", response_model=list[PitchOut], dependencies=[Depends(require_admin)])
async def list_pitches(db: AsyncSession = Depends(get_db)):
    """Fetches all pitches for the Admin Dashboard"""
    result = await db.execute(select(Pitch).order_by(Pitch.created_at.desc()))
    return result.scalars().all()

@router.patch("/{id}/status", response_model=PitchOut, dependencies=[Depends(require_admin)])
async def update_pitch_status(
    id: int, 
    status: str = Query(...), 
    db: AsyncSession = Depends(get_db)
):
    """Handles Approve/Reject button clicks from the Admin Dashboard"""
    if status not in ("pending", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.execute(select(Pitch).where(Pitch.id == id))
    record = result.scalar_one_or_none()
    
    if not record:
        raise HTTPException(status_code=404, detail="Pitch not found")
    
    record.status = status
    await db.commit()
    await db.refresh(record)
    return record