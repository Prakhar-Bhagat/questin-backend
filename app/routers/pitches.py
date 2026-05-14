from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.pitch import PitchIn, PitchOut
from app.services import pitches as svc
from fastapi import Request
from app.limiter import limiter

router = APIRouter()

@router.post("/", response_model=PitchOut, status_code=201)
@limiter.limit("3/minute")
async def submit_pitch(request: Request, data: PitchIn, db: AsyncSession = Depends(get_db)):
    return await svc.create_pitch(data, db)