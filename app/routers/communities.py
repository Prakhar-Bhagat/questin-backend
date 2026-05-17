from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.community import Community
from app.schemas.community import CommunityOut
from app.auth import require_approved_venue
from app.models.users import User
router = APIRouter()

@router.get("/", response_model=list[CommunityOut])
async def get_communities(
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_approved_venue),   # <-- protected
):
    query = select(Community).where(Community.is_active == True)
    if category:
        query = query.where(Community.category == category)
    result = await db.execute(query)
    return result.scalars().all()