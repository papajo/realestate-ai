from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional

from app.core.database import get_db
from app.models.user import User
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdate
from app.api.v1.endpoints.auth import get_current_user
from app.core.encryption import kms_encryption

router = APIRouter()


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_data: LeadCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Encrypt PII - returns bytes
    encrypted_data = kms_encryption.encrypt_pii({
        "email": lead_data.owner_email,
        "phone": lead_data.owner_phone,
        "name": lead_data.owner_name
    })
    
    # Convert bytes to base64 string for storage
    import base64
    owner_name_b64 = None
    owner_email_b64 = None
    owner_phone_b64 = None
    
    if encrypted_data.get("name"):
        owner_name_b64 = base64.b64encode(encrypted_data.get("name")).decode() if isinstance(encrypted_data.get("name"), bytes) else encrypted_data.get("name")
    if encrypted_data.get("email"):
        owner_email_b64 = base64.b64encode(encrypted_data.get("email")).decode() if isinstance(encrypted_data.get("email"), bytes) else encrypted_data.get("email")
    if encrypted_data.get("phone"):
        owner_phone_b64 = base64.b64encode(encrypted_data.get("phone")).decode() if isinstance(encrypted_data.get("phone"), bytes) else encrypted_data.get("phone")
    
    new_lead = Lead(
        user_id=current_user.id,
        property_address=lead_data.property_address,
        property_city=lead_data.property_city,
        property_state=lead_data.property_state,
        property_zip=lead_data.property_zip,
        owner_name=owner_name_b64,
        owner_email=owner_email_b64,
        owner_phone=owner_phone_b64,
        source="manual"
    )
    
    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)
    
    # Decrypt PII for response
    if new_lead.owner_name or new_lead.owner_email or new_lead.owner_phone:
        import base64
        decrypted_name = None
        decrypted_email = None
        decrypted_phone = None
        
        if new_lead.owner_name:
            decrypted_name = kms_encryption.decrypt(base64.b64decode(new_lead.owner_name))
        if new_lead.owner_email:
            decrypted_email = kms_encryption.decrypt(base64.b64decode(new_lead.owner_email))
        if new_lead.owner_phone:
            decrypted_phone = kms_encryption.decrypt(base64.b64decode(new_lead.owner_phone))
        
        new_lead.owner_name = decrypted_name
        new_lead.owner_email = decrypted_email
        new_lead.owner_phone = decrypted_phone
    
    return new_lead


@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = None,
    min_score: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Lead).where(Lead.user_id == current_user.id)
    
    if status_filter:
        query = query.where(Lead.status == status_filter)
    
    if min_score is not None:
        query = query.where(Lead.lead_score >= min_score)
    
    query = query.order_by(desc(Lead.lead_score)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    leads = result.scalars().all()
    
    # Decrypt PII for each lead
    import base64
    for lead in leads:
        if lead.owner_name or lead.owner_email or lead.owner_phone:
            try:
                decrypted_name = None
                decrypted_email = None
                decrypted_phone = None
                
                if lead.owner_name:
                    decrypted_name = kms_encryption.decrypt(base64.b64decode(lead.owner_name))
                if lead.owner_email:
                    decrypted_email = kms_encryption.decrypt(base64.b64decode(lead.owner_email))
                if lead.owner_phone:
                    decrypted_phone = kms_encryption.decrypt(base64.b64decode(lead.owner_phone))
                
                lead.owner_name = decrypted_name
                lead.owner_email = decrypted_email
                lead.owner_phone = decrypted_phone
            except Exception:
                # If decryption fails, leave values as is
                pass
    
    return leads


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.user_id == current_user.id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Decrypt PII
    if lead.owner_name or lead.owner_email or lead.owner_phone:
        import base64
        try:
            decrypted_name = None
            decrypted_email = None
            decrypted_phone = None
            
            if lead.owner_name:
                decrypted_name = kms_encryption.decrypt(base64.b64decode(lead.owner_name))
            if lead.owner_email:
                decrypted_email = kms_encryption.decrypt(base64.b64decode(lead.owner_email))
            if lead.owner_phone:
                decrypted_phone = kms_encryption.decrypt(base64.b64decode(lead.owner_phone))
            
            lead.owner_name = decrypted_name
            lead.owner_email = decrypted_email
            lead.owner_phone = decrypted_phone
        except Exception:
            # If decryption fails, leave values as is
            pass
    
    return lead


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.user_id == current_user.id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    if lead_update.status:
        lead.status = lead_update.status
    if lead_update.lead_score is not None:
        lead.lead_score = lead_update.lead_score
    if lead_update.distress_signals:
        lead.distress_signals = lead_update.distress_signals
    
    await db.commit()
    await db.refresh(lead)
    
    return lead


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.user_id == current_user.id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    await db.delete(lead)
    await db.commit()
    
    return None

