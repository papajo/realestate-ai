from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Dict

from app.core.database import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.services.no_code_builder import NoCodeBuilderService

router = APIRouter()


class ToolDescription(BaseModel):
    description: str
    tool_type: Optional[str] = None


class ToolResponse(BaseModel):
    tool_id: str
    name: str
    code: str
    preview: str


@router.post("/generate", response_model=ToolResponse)
async def generate_tool(
    tool_desc: ToolDescription,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a tool from natural language description"""
    builder_service = NoCodeBuilderService()
    
    try:
        tool = await builder_service.generate_tool(
            description=tool_desc.description,
            tool_type=tool_desc.tool_type,
            user_id=current_user.id
        )
        
        return tool
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool generation failed: {str(e)}")


@router.get("/list")
async def list_tools(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all tools created by the user"""
    builder_service = NoCodeBuilderService()
    tools = await builder_service.list_user_tools(user_id=current_user.id)
    
    return {"tools": tools}


@router.get("/{tool_id}")
async def get_tool(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific tool"""
    builder_service = NoCodeBuilderService()
    tool = await builder_service.get_tool(tool_id=tool_id, user_id=current_user.id)
    
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    return tool

