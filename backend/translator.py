import httpx
import os
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.models.translations import Translation
from backend.models.ads_keyword import ADSKeyword
from backend.database import SessionLocal

TRANSLATE_URL = os.getenv("TRANSLATE_URL", "")
TRANSLATE_API_KEY = os.getenv("TRANSLATE_API_KEY", "")


class BaseTranslator:
    def __init__(self, db: Session, text: str, target_lang: str = "uk"):
        self.db = db
        self.text = text.lower()
        self.target_lang = target_lang
        self.translation = None
        self.original_language = None

    def translate_text(self):
        pass

    def get_translate(self):
        translation = self.db.query(Translation).filter_by(
            original_text=self.text
        ).first()
        if translation:
            return {
                "translation": translation.translated_text,
                "original_language": translation.detected_language,
            }

        self.translate_text()
        if self.translation and self.original_language:
            return {
                "translation": self.translation,
                "original_language": self.original_language,
            }

        return None


class Translator(BaseTranslator):
    def translate_text(self):
        if not TRANSLATE_URL or not TRANSLATE_API_KEY:
            return
        try:
            with httpx.Client(timeout=60) as client:
                response = client.post(
                    TRANSLATE_URL,
                    json={
                        "q": self.text,
                        "source": "auto",
                        "target": self.target_lang,
                        "format": "text",
                        "api_key": TRANSLATE_API_KEY,
                    },
                )
                response.raise_for_status()
                data = response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
            return

        translated_text = data.get("translatedText")
        detected_lang = data.get("detectedLanguage", {}).get("language")

        if translated_text and detected_lang:
            self.translation = translated_text
            self.original_language = detected_lang
            new_translation = Translation(
                original_text=self.text,
                translated_text=self.translation,
                detected_language=self.original_language)
            self.db.add(new_translation)


def add_translations():
    db = SessionLocal()
    keywords = db.query(ADSKeyword).filter(
        or_(
            ADSKeyword.translation.is_(None),
            ADSKeyword.translation == ""
        )
    ).all()

    for keyword in keywords:
        translator = Translator(db, keyword.keyword)
        new_translation = translator.get_translate()
        if new_translation:
            keyword.translation = new_translation["translation"]
            keyword.original_language = new_translation["original_language"]
    db.commit()
