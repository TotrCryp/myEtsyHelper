from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, unique=True, index=True)
    title = Column(String, index=True)
    url = Column(String)
    ads_keywords = relationship("ADSKeyword", back_populates="listing")
