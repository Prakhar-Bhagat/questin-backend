from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.pitch import PitchIn, PitchOut
from app.services import pitches as svc

router = APIRouter()

@router.post("/", response_model=PitchOut, status_code=201)
async def submit_pitch(data: PitchIn, db: AsyncSession = Depends(get_db)):
    return await svc.create_pitch(data, db)