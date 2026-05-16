from datetime import datetime  # Need this for the type hint
from typing import Optional    # Need this for nullable fields
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Pitch(Base):
    __tablename__ = "pitches"

    id: Mapped[int] = mapped_column(primary_key=True)
    community_name: Mapped[str] = mapped_column(String(100))
    organizer_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(1000))
    category: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="pending")    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    group_size: Mapped[Optional[str]] = mapped_column(String(50))
    price_range: Mapped[Optional[str]] = mapped_column(String(50))
    duration: Mapped[Optional[str]] = mapped_column(String(50))
    frequency: Mapped[Optional[str]] = mapped_column(String(50))