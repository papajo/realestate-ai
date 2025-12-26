from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class LeadBase(BaseModel):
    property_address: str
    property_city: str
    property_state: str
    property_zip: str
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    owner_phone: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    lead_score: Optional[float] = None
    distress_signals: Optional[Dict] = None


class LeadResponse(LeadBase):
    id: int
    user_id: int
    lead_score: float
    distress_signals: Dict
    status: str
    source: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ConversationMessage(BaseModel):
    role: str  # user, assistant
    content: str
    timestamp: datetime


class ConversationCreate(BaseModel):
    lead_id: int
    message: str


class ConversationResponse(BaseModel):
    id: int
    lead_id: int
    messages: List[Dict]
    qualification_status: str
    qualification_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class PropertyAnalysisResponse(BaseModel):
    id: int
    lead_id: int
    detected_issues: List[Dict]
    repair_cost_estimate: float
    images_analyzed: int
    created_at: datetime
    
    class Config:
        from_attributes = True

