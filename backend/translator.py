import httpx
import os
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.models.translations import Translation
from backend.models.ads_keyword import ADSKeyword

LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL", "http://localhost:5000/translate")
LIBRETRANSLATE_API_KEY = os.getenv("LIBRETRANSLATE_API_KEY", "")


def translate_text(text: str, target_lang: str = "uk"):
    with httpx.Client() as client:
        response = client.post(
            LIBRETRANSLATE_URL,
            json={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text",
                "alternatives": 1,
                "api_key": LIBRETRANSLATE_API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        return data


def get_translate(db: Session, text: str):

    translation = db.query(Translation).filter_by(
        original_text=text
    ).first()

    if translation:
        return {
            "translation": translation.translated_text,
            "original_language": translation.detected_language,
        }

    data = translate_text(text)
    detected = data.get("detectedLanguage")
    new_translation = Translation(
        original_text=text,
        translated_text=data["translatedText"],
        detected_language=detected.get("language") if isinstance(detected, dict) else None
    )
    db.add(new_translation)
    db.commit()
    db.refresh(new_translation)

    return {
        "translation": new_translation.translated_text,
        "original_language": new_translation.detected_language,
    }


def add_translations(db: Session):
    keywords = db.query(ADSKeyword).filter(
        or_(
            ADSKeyword.translation.is_(None),
            ADSKeyword.translation == ""
        )
    ).all()

    for keyword in keywords:
        result = get_translate(db, keyword.keyword)
        keyword.translation = result["translation"]
        keyword.original_language = result.get("original_language")

    db.commit()
