from datetime import datetime
from pydantic import BaseModel, field_validator
    
class VenueRequestIn(BaseModel):
    community_id: int
    poc: str           # maps to requestForm.poc
    phone: str
    dates: str         # maps to requestForm.dates
    capacity: str
    revenue: str       # maps to requestForm.revenue
    notes: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        digits = ''.join(filter(str.isdigit, v))

        if len(digits) != 10:
            raise ValueError("Phone number must be 10 digits")

        return digits

class VenueRequestOut(BaseModel):
    id: int
    community_id: int
    poc_name: str
    email: str
    phone: str
    preferred_dates: str
    capacity: str
    revenue_model: str
    notes: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}