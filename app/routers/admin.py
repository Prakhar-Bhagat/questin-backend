from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.users import User
from app.auth import require_admin

router = APIRouter()


# ---------- schemas ----------

class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_approved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ApproveRequest(BaseModel):
    is_approved: bool


# ---------- endpoints ----------

@router.get("/users", response_model=List[UserOut], dependencies=[Depends(require_admin)])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()


@router.patch("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
async def update_user_approval(
    user_id: int,
    body: ApproveRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_approved = body.is_approved
    await db.commit()
    await db.refresh(user)
    return user