from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Column
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class VenueRequest(Base):
    __tablename__ = "venue_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    community_id: Mapped[int] = mapped_column(Integer, ForeignKey("communities.id"))
    poc_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    preferred_dates: Mapped[str] = mapped_column(String(200))
    capacity: Mapped[str] = mapped_column(String(50))
    revenue_model: Mapped[str] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())