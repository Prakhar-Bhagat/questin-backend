from pydantic import BaseModel

class CommunityOut(BaseModel):
    id: int
    name: str
    tagline: str
    category: str
    group_size: str
    price_range: str
    duration: str
    venue_needs: str
    frequency: str
    image_url: str

    model_config = {"from_attributes": True}