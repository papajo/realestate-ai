from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import io

from app.core.database import get_db
from app.models.user import User
from app.models.lead import Lead, PropertyAnalysis
from app.schemas.lead import PropertyAnalysisResponse
from app.api.v1.endpoints.auth import get_current_user
from app.services.property_analysis import PropertyAnalysisService

router = APIRouter()


@router.post("/analyze/{lead_id}", response_model=PropertyAnalysisResponse)
async def analyze_property(
    lead_id: int,
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify lead exists and belongs to user
    from sqlalchemy import select
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.user_id == current_user.id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Analyze images
    analysis_service = PropertyAnalysisService()
    all_issues = []
    total_cost = 0.0
    
    for image in images:
        image_bytes = await image.read()
        analysis_result = await analysis_service.analyze_image(image_bytes)
        
        all_issues.extend(analysis_result.get("issues", []))
        total_cost += analysis_result.get("estimated_cost", 0.0)
    
    # Create or update property analysis
    result = await db.execute(
        select(PropertyAnalysis).where(PropertyAnalysis.lead_id == lead_id)
    )
    property_analysis = result.scalar_one_or_none()
    
    if property_analysis:
        property_analysis.detected_issues = all_issues
        property_analysis.repair_cost_estimate = total_cost
        property_analysis.images_analyzed += len(images)
    else:
        property_analysis = PropertyAnalysis(
            lead_id=lead_id,
            detected_issues=all_issues,
            repair_cost_estimate=total_cost,
            images_analyzed=len(images)
        )
        db.add(property_analysis)
    
    await db.commit()
    await db.refresh(property_analysis)
    
    return property_analysis


@router.get("/{lead_id}", response_model=PropertyAnalysisResponse)
async def get_property_analysis(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify lead belongs to user
    from sqlalchemy import select
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.user_id == current_user.id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    result = await db.execute(
        select(PropertyAnalysis).where(PropertyAnalysis.lead_id == lead_id)
    )
    property_analysis = result.scalar_one_or_none()
    
    if not property_analysis:
        raise HTTPException(status_code=404, detail="Property analysis not found")
    
    return property_analysis

