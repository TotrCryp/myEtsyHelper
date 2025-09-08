from pydantic import BaseModel, Field, constr
from typing import Optional
from .listing import ListingOut


class ADSKeywordBase(BaseModel):
    keyword: constr(strip_whitespace=True, min_length=2, max_length=100)
    listing_id: int = Field(..., gt=0, description="ID лістингу (має існувати)")
    views: int = 0
    clicks: int = 0
    click_rate: float = 0.0
    orders: int = 0
    revenue: float = 0.0
    spend: float = 0.0
    roas: float = 0.0
    ad: bool = False
    approved: bool = False


class ADSKeywordCreate(ADSKeywordBase):
    translation: Optional[str] = None
    original_language: Optional[str] = None


class ADSKeywordOut(ADSKeywordBase):
    id: int
    translation: Optional[str] = None
    original_language: Optional[str] = None
    listing: Optional[ListingOut] = None

    class Config:
        from_attributes = True
