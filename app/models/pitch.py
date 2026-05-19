from datetime import datetime  
from typing import Optional    
from sqlalchemy import String, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Pitch(Base):
    __tablename__ = "pitches"

    id: Mapped[int] = mapped_column(primary_key=True)
    community_name: Mapped[str] = mapped_column(String(100))
    organizer_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    venue_needs: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    group_size: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    price_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    duration: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    frequency: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)