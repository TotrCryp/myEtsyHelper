from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class ADSKeyword(Base):
    __tablename__ = "ads_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    translation = Column(String, nullable=True)
    original_language = Column(String, nullable=True)
    listing_id = Column(Integer, ForeignKey("listings.listing_id"))
    views = Column(Integer)
    clicks = Column(Integer)
    click_rate = Column(Float)
    orders = Column(Integer)
    revenue = Column(Float)
    spend = Column(Float)
    roas = Column(Float)
    ad = Column(Boolean)
    approved = Column(Boolean)
    listing = relationship("Listing", back_populates="ads_keywords")
