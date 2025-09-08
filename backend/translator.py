import httpx
import os
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.models.translations import Translation
from backend.models.ads_keyword import ADSKeyword
from backend.database import SessionLocal


class BaseTranslator:
    def __init__(self, db: Session, text: str, target_lang: str = "uk",  **kwargs):
        self.db = db
        self.text = text
        self.target_lang = target_lang
        self.translation = None
        self.original_language = None

    def translate_text(self, **kwargs):
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
    pass


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
