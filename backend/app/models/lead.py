from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Lead information
    property_address = Column(String, nullable=False, index=True)
    property_city = Column(String, nullable=False)
    property_state = Column(String, nullable=False)
    property_zip = Column(String, nullable=False)
    
    # Owner information (encrypted)
    owner_name = Column(Text, nullable=True)
    owner_email = Column(Text, nullable=True)
    owner_phone = Column(Text, nullable=True)
    
    # Lead scoring
    lead_score = Column(Float, default=0.0, index=True)
    distress_signals = Column(JSON, default=dict)
    
    # Status
    status = Column(String, default="new")  # new, qualified, contacted, converted, lost
    source = Column(String, nullable=True)  # list_stacking, manual, referral
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    conversations = relationship("Conversation", back_populates="lead")
    property_analyses = relationship("PropertyAnalysis", back_populates="lead")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Conversation data
    messages = Column(JSON, default=list)
    qualification_status = Column(String, default="pending")  # pending, qualified, not_qualified
    qualification_score = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="conversations")


class PropertyAnalysis(Base):
    __tablename__ = "property_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    # Analysis results
    detected_issues = Column(JSON, default=list)
    repair_cost_estimate = Column(Float, default=0.0)
    images_analyzed = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="property_analyses")

