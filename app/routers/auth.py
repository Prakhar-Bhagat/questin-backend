from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
import secrets

from app.database import get_db
from app.models.users import User
from app.auth import hash_password, verify_password, create_access_token
from app.limiter import limiter
from app.services.email import send_verification_email

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_approved: bool
    is_verified: bool
    role: str


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register(request: Request, body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    if len(body.password) < 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must be at least 8 characters")

    verify_token = secrets.token_urlsafe(32)

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        name=body.name,
        role="venue",
        is_approved=False,
        is_verified=False,
        verify_token=verify_token,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    await send_verification_email(user.email, user.name or "", verify_token)

    token = create_access_token(user.id, user.role)
    return AuthResponse(
        access_token=token,
        is_approved=user.is_approved,
        is_verified=user.is_verified,
        role=user.role,
    )


@router.post("/login", response_model=AuthResponse)
@limiter.limit("20/minute")
async def login(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(user.id, user.role)
    return AuthResponse(
        access_token=token,
        is_approved=user.is_approved,
        is_verified=user.is_verified,
        role=user.role,
    )


@router.get("/verify")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.verify_token == token))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification link")

    user.is_verified = True
    user.verify_token = None
    await db.commit()

    return {"message": "Email verified. We'll review your account and be in touch within 24 hours."}