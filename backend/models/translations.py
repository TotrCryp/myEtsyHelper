from sqlalchemy import Column, String, Integer
from backend.database import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String, index=True, nullable=False)
    translated_text = Column(String, nullable=False)
    detected_language = Column(String, nullable=False)
