from pydantic import BaseModel, EmailStr
from datetime import datetime

class PitchIn(BaseModel):
    community_name: str
    organizer_name: str
    email: EmailStr
    description: str
    category: str

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