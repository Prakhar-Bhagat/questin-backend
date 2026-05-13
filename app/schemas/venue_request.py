from pydantic import BaseModel
from datetime import datetime

class VenueRequestIn(BaseModel):
    community_id: int
    poc: str           # maps to requestForm.poc
    phone: str
    dates: str         # maps to requestForm.dates
    capacity: str
    revenue: str       # maps to requestForm.revenue
    notes: str | None = None

class VenueRequestOut(BaseModel):
    id: int
    community_id: int
    poc_name: str
    phone: str
    preferred_dates: str
    capacity: str
    revenue_model: str
    notes: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}