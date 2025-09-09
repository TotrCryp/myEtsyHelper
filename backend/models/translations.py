from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates
from backend.database import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String, index=True, nullable=False)
    translated_text = Column(String, nullable=False)
    detected_language = Column(String, nullable=False)

    @validates('original_text', 'translated_text', 'detected_language')
    def convert_lower(self, key, value):
        if value is not None:
            return value.lower()
        return value
