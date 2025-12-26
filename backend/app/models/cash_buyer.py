from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class CashBuyer(Base):
    __tablename__ = "cash_buyers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Buyer information
    name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    email = Column(Text, nullable=True)  # Encrypted
    phone = Column(Text, nullable=True)  # Encrypted
    
    # Location
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    
    # Buying criteria
    preferred_property_types = Column(JSON, default=list)
    price_range_min = Column(Float, nullable=True)
    price_range_max = Column(Float, nullable=True)
    investment_areas = Column(JSON, default=list)
    
    # Activity
    total_purchases = Column(Integer, default=0)
    average_purchase_price = Column(Float, nullable=True)
    last_purchase_date = Column(DateTime, nullable=True)
    
    # Vector embedding for similarity search
    embedding = Column(JSON, nullable=True)
    
    # Metadata
    source = Column(String, nullable=True)  # scraper, manual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

