from pydantic import BaseModel, Field, constr


class ListingBase(BaseModel):
    listing_id: int = Field(..., gt=0, description="ID лістингу (має існувати)")  # зовнішній ID з Etsy
    title: constr(strip_whitespace=True, min_length=2, max_length=500)
    url: constr(strip_whitespace=True, min_length=2, max_length=1000)


class ListingCreate(ListingBase):
    pass


class ListingOut(ListingBase):
    id: int  # внутрішній primary key

    class Config:
        from_attributes = True
