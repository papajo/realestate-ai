from fastapi import APIRouter
from app.api.v1.endpoints import auth, leads, chatbot, property_analysis, cash_buyers, list_stacking, tools

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(property_analysis.router, prefix="/property-analysis", tags=["property-analysis"])
api_router.include_router(cash_buyers.router, prefix="/cash-buyers", tags=["cash-buyers"])
api_router.include_router(list_stacking.router, prefix="/list-stacking", tags=["list-stacking"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])

