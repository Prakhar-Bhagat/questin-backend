from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Community(Base):
    __tablename__ = "communities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    tagline: Mapped[str] = mapped_column(String(300))
    category: Mapped[str] = mapped_column(String(50))
    group_size: Mapped[str] = mapped_column(String(50))
    price_range: Mapped[str] = mapped_column(String(50))
    duration: Mapped[str] = mapped_column(String(50))
    venue_needs: Mapped[str] = mapped_column(String(300))
    frequency: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())