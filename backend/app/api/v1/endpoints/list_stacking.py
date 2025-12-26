from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
import httpx

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.lead import Lead
from app.api.v1.endpoints.auth import get_current_user
from app.services.list_stacking import ListStackingService
from app.services.lead_scoring import LeadScoringService

router = APIRouter()


@router.post("/search")
async def search_properties(
    address: str,
    city: str,
    state: str,
    zip_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """Search for properties using list stacking with public records"""
    list_stacking_service = ListStackingService()
    
    try:
        # Fetch public record data
        property_data = await list_stacking_service.fetch_property_data(
            address=address,
            city=city,
            state=state,
            zip_code=zip_code
        )
        
        # Detect distress signals
        distress_signals = await list_stacking_service.detect_distress_signals(property_data)
        
        # Score the lead
        scoring_service = LeadScoringService()
        lead_score = await scoring_service.score_lead(distress_signals)
        
        # Create lead if score is above threshold
        if lead_score >= 0.5:
            new_lead = Lead(
                user_id=current_user.id,
                property_address=address,
                property_city=city,
                property_state=state,
                property_zip=zip_code,
                lead_score=lead_score,
                distress_signals=distress_signals,
                source="list_stacking"
            )
            
            db.add(new_lead)
            await db.commit()
            await db.refresh(new_lead)
            
            return {
                "lead_id": new_lead.id,
                "lead_score": lead_score,
                "distress_signals": distress_signals,
                "property_data": property_data
            }
        
        return {
            "lead_score": lead_score,
            "distress_signals": distress_signals,
            "property_data": property_data,
            "message": "Lead score below threshold, not created"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"List stacking failed: {str(e)}")


@router.post("/batch-search")
async def batch_search_properties(
    properties: List[Dict],
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Batch search for multiple properties"""
    list_stacking_service = ListStackingService()
    results = []
    
    for prop in properties:
        try:
            property_data = await list_stacking_service.fetch_property_data(
                address=prop.get("address"),
                city=prop.get("city"),
                state=prop.get("state"),
                zip_code=prop.get("zip_code")
            )
            
            distress_signals = await list_stacking_service.detect_distress_signals(property_data)
            scoring_service = LeadScoringService()
            lead_score = await scoring_service.score_lead(distress_signals)
            
            results.append({
                "address": prop.get("address"),
                "lead_score": lead_score,
                "distress_signals": distress_signals
            })
        except Exception as e:
            results.append({
                "address": prop.get("address"),
                "error": str(e)
            })
    
    return {"results": results}

