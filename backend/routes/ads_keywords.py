from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from typing import Union, List
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.ads_keyword import ADSKeyword
from backend.models.listing import Listing
from backend.schemas.ads_keyword import ADSKeywordCreate, ADSKeywordOut
from ..auth import get_token
from ..translator import add_translations

router = APIRouter(prefix="/ads-keywords",
                   tags=["ADS keywords"],
                   dependencies=[Depends(get_token)])


@router.get("/", response_model=list[ADSKeywordOut])
def get_ads_keywords(
    listing_id: int | None = Query(None, description="ID лістингу для фільтрації"),
    approved: bool | None = Query(None, description="Фільтрувати за статусом approved"),
    db: Session = Depends(get_db)
):
    query = db.query(ADSKeyword)

    if listing_id is not None:
        query = query.filter(ADSKeyword.listing_id == listing_id)

    if approved is not None:
        query = query.filter(ADSKeyword.approved == approved)

    return query.all()


@router.post("/", response_model=list[ADSKeywordOut])
def create_ads_keyword(
    background_tasks: BackgroundTasks,
    data: Union[ADSKeywordCreate, List[ADSKeywordCreate]],
    db: Session = Depends(get_db)
):

    if isinstance(data, ADSKeywordCreate):
        data = [data]

    new_keywords = []

    for item in data:

        existing = db.query(Listing).filter(Listing.listing_id == item.listing_id).first()
        if not existing:
            raise HTTPException(
                status_code=400,
                detail=f"Listing with listing_id={item.listing_id} does not exist"
            )

        new_kw = ADSKeyword(
            keyword=item.keyword,
            listing_id=item.listing_id,
            views=item.views,
            clicks=item.clicks,
            click_rate=item.click_rate,
            orders=item.orders,
            revenue=item.revenue,
            spend=item.spend,
            roas=item.roas,
            ad=item.ad,
            approved=item.approved,
        )
        db.add(new_kw)
        new_keywords.append(new_kw)

    db.commit()
    for kw in new_keywords:
        db.refresh(kw)

    background_tasks.add_task(add_translations, db)

    return new_keywords
