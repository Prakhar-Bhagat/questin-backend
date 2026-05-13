from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.waitlist import WaitlistIn, WaitlistOut
from app.services import waitlist as svc

router = APIRouter()

@router.post("/", response_model=WaitlistOut, status_code=201)
async def join_waitlist(data: WaitlistIn, db: AsyncSession = Depends(get_db)):
    return await svc.add_to_waitlist(data, db)