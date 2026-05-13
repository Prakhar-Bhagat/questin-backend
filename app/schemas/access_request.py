from pydantic import BaseModel, EmailStr
from datetime import datetime

class AccessRequestIn(BaseModel):
    name: str
    email: EmailStr
    about: str
    user_type: str  # "venue" | "brand"

class AccessRequestOut(BaseModel):
    id: int
    name: str
    email: str
    about: str
    user_type: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}

class AccessRequestStatusUpdate(BaseModel):
    request: AccessRequestOut
    token: str | None = None