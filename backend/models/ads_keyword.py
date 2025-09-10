import enum
from sqlalchemy import Column, Enum as SQLEnum, Integer, String, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base


class KeywordStatus(enum.Enum):
    NEW = "New"
    APPROVED = "Approved"
    REJECTED = "Rejected"


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
    status = Column(SQLEnum(KeywordStatus), default=KeywordStatus.NEW, nullable=False)
    listing = relationship("Listing", back_populates="ads_keywords")

    __table_args__ = (
        UniqueConstraint("listing_id", "keyword", name="uix_listing_keyword"),
    )
