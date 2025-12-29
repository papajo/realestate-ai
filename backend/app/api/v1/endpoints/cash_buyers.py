from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.models.cash_buyer import CashBuyer
from app.api.v1.endpoints.auth import get_current_user
from app.services.cash_buyer_scraper import CashBuyerScraperService

router = APIRouter()


class ScrapeRequest(BaseModel):
    location: str
    limit: int = 100


@router.post("/scrape")
async def scrape_cash_buyers(
    request: ScrapeRequest,
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Scrape cash buyers from public records"""
    scraper_service = CashBuyerScraperService()
    
    # Run scraping in background
    background_tasks.add_task(
        scraper_service.scrape_and_store,
        location=request.location,
        limit=request.limit
    )
    
    return {
        "message": "Cash buyer scraping started",
        "location": request.location,
        "limit": request.limit
    }


@router.get("/", response_model=List[dict])
async def get_cash_buyers(
    city: Optional[str] = None,
    state: Optional[str] = None,
    min_purchases: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get cash buyers with filters"""
    query = select(CashBuyer)
    
    if city:
        query = query.where(CashBuyer.city == city)
    if state:
        query = query.where(CashBuyer.state == state)
    if min_purchases:
        query = query.where(CashBuyer.total_purchases >= min_purchases)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    buyers = result.scalars().all()
    
    return [
        {
            "id": buyer.id,
            "name": buyer.name,
            "company_name": buyer.company_name,
            "city": buyer.city,
            "state": buyer.state,
            "total_purchases": buyer.total_purchases,
            "average_purchase_price": buyer.average_purchase_price,
            "preferred_property_types": buyer.preferred_property_types
        }
        for buyer in buyers
    ]


@router.post("/search-similar")
async def search_similar_buyers(
    criteria: dict,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search for similar cash buyers using vector similarity"""
    from app.services.vector_search import VectorSearchService
    
    vector_service = VectorSearchService()
    similar_buyers = await vector_service.search_similar_buyers(
        criteria=criteria,
        limit=limit
    )
    
    return {"results": similar_buyers}

