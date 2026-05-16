from pydantic import BaseModel, EmailStr
from datetime import datetime

class PitchIn(BaseModel):
    community_name: str
    organizer_name: str
    email: EmailStr
    description: str
    category: str
    group_size: str | None = None
    price_range: str | None = None
    duration: str | None = None
    frequency: str | None = None
    venue_needs: str | None = None

class PitchOut(BaseModel):
    id: int
    community_name: str
    organizer_name: str
    email: str
    description: str
    category: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}