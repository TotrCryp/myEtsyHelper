from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.listing import Listing
from backend.schemas.listing import ListingCreate, ListingOut
from backend.auth import get_token

router = APIRouter(prefix="/listings",
                   tags=["Listings"],
                   dependencies=[Depends(get_token)])


@router.get("/", response_model=list[ListingOut])
def get_listings(listing_id: int | None = Query(None, description="ID лістингу для фільтрації"),
                 db: Session = Depends(get_db)):

    query = db.query(Listing)

    if listing_id is not None:
        query = query.filter(Listing.listing_id == listing_id)

    return query.all()


@router.post("/", response_model=ListingOut)
def create_listing(data: ListingCreate,
                   db: Session = Depends(get_db)):
    new_listing = Listing(listing_id=data.listing_id,
                          title=data.title,
                          url=data.url)

    existing = db.query(Listing).filter(Listing.listing_id == data.listing_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Listing with listing_id={data.listing_id} already exists"
        )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing
