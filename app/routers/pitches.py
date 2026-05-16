from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.pitch import PitchIn, PitchOut
from app.services import pitches as svc
from app.models.pitch import Pitch
from app.auth import require_admin   
from app.limiter import limiter
from app.models.community import Community
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

@router.patch("/{id}/status", dependencies=[Depends(require_admin)])
async def update_pitch_status(
    id: int, 
    status: str = Query(...), 
    db: AsyncSession = Depends(get_db)
):
    if status not in ("pending", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.execute(select(Pitch).where(Pitch.id == id))
    record = result.scalar_one_or_none()
    
    if not record:
        raise HTTPException(status_code=404, detail="Pitch not found")
    
    # 1. Update the pitch status
    record.status = status
    
    # 2. THE BRIDGE: If approved, auto-create the Community
    if status == "approved":
        # Check if it already exists so we don't make duplicates if you click twice
        existing = await db.execute(select(Community).where(Community.name == record.community_name))
        
        if not existing.scalar_one_or_none():
            new_community = Community(
                name=record.community_name,
                tagline=(record.description[:297] + '...') if len(record.description) > 300 else record.description,
                category=record.category,                
                group_size=record.group_size or "Varies",
                price_range=record.price_range or "Free",
                duration=record.duration or "1-2 hours",
                frequency=record.frequency or "Monthly",
                image_url="",
                venue_needs=f"Space matching '{record.category.split(',')[0]}' context",
                is_active=True
            )
            db.add(new_community)

    await db.commit()
    await db.refresh(record)
    return record