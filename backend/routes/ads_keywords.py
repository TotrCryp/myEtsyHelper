from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from typing import Union, List
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.ads_keyword import ADSKeyword, KeywordStatus
from backend.models.listing import Listing
from backend.schemas.ads_keyword import ADSKeywordCreate, ADSKeywordOut
from ..auth import get_token
from ..translator import Translation, Translator, add_translations

router = APIRouter(prefix="/ads-keywords",
                   tags=["ADS keywords"],
                   dependencies=[Depends(get_token)])


@router.get("/", response_model=list[ADSKeywordOut])
def get_ads_keywords(
    listing_id: int | None = Query(None, description="ID лістингу для фільтрації"),
    status: str | None = Query(None, description="Фільтрувати за статусом"),
    db: Session = Depends(get_db)
):
    query = db.query(ADSKeyword)

    if listing_id is not None:
        query = query.filter(ADSKeyword.listing_id == listing_id)

    if status is not None:
        query = query.filter(ADSKeyword.status == status.upper())

    return query.all()


@router.post("/", response_model=list[ADSKeywordOut])
def create_ads_keyword(
    background_tasks: BackgroundTasks,
    data: Union[ADSKeywordCreate, List[ADSKeywordCreate]],
    db: Session = Depends(get_db)
):

    new_keywords = []

    if isinstance(data, ADSKeywordCreate):
        data = [data]

    seen: set[tuple[int, str]] = set()
    unique_items = []

    for item in data:
        key = (item.listing_id, item.keyword)
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    for item in unique_items:

        existing_listing = db.query(Listing).filter(Listing.listing_id == item.listing_id).first()
        if not existing_listing:
            raise HTTPException(
                status_code=400,
                detail=f"Listing with listing_id={item.listing_id} does not exist"
            )

        existing_kw = db.query(ADSKeyword).filter(ADSKeyword.listing_id == item.listing_id,
                                                  ADSKeyword.keyword == item.keyword).first()
        if existing_kw:
            existing_kw.views = item.views
            existing_kw.clicks = item.clicks
            existing_kw.click_rate = item.click_rate
            existing_kw.orders = item.orders
            existing_kw.revenue = item.revenue
            existing_kw.spend = item.spend
            existing_kw.roas = item.roas
            existing_kw.ad = item.ad
            existing_kw.status = item.status
            new_keywords.append(existing_kw)
        else:
            new_kw = ADSKeyword(
                keyword=item.keyword,
                translation=item.translation,
                original_language=item.original_language,
                listing_id=item.listing_id,
                views=item.views,
                clicks=item.clicks,
                click_rate=item.click_rate,
                orders=item.orders,
                revenue=item.revenue,
                spend=item.spend,
                roas=item.roas,
                ad=item.ad,
                status=KeywordStatus.NEW,
            )
            db.add(new_kw)
            new_keywords.append(new_kw)
            if new_kw.translation and new_kw.original_language:
                new_translation = Translation(
                    original_text=new_kw.keyword,
                    translated_text=new_kw.translation,
                    detected_language=new_kw.original_language)
                db.add(new_translation)
            # else:
            #     translator = Translator(db, new_kw.keyword)
            #     new_translation = translator.get_translate()
            #     if new_translation:
            #         new_kw.translation = new_translation.translation
            #         new_kw.original_language = new_translation.original_language

    db.commit()
    for kw in new_keywords:
        db.refresh(kw)

    background_tasks.add_task(add_translations)

    return new_keywords
