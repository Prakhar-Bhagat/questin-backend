from pydantic import BaseModel, EmailStr
from datetime import datetime

class WaitlistIn(BaseModel):
    email: EmailStr

class WaitlistOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}