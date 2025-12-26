from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.lead import Lead, Conversation
from app.schemas.lead import ConversationCreate, ConversationResponse
from app.api.v1.endpoints.auth import get_current_user
from app.services.chatbot import ChatbotService

router = APIRouter()


@router.post("/conversation", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify lead exists and belongs to user
    from sqlalchemy import select
    result = await db.execute(
        select(Lead).where(Lead.id == conversation_data.lead_id, Lead.user_id == current_user.id)
    )
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Get or create conversation
    result = await db.execute(
        select(Conversation).where(
            Conversation.lead_id == conversation_data.lead_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        conversation = Conversation(
            lead_id=conversation_data.lead_id,
            user_id=current_user.id,
            messages=[]
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
    
    # Process message with chatbot
    chatbot_service = ChatbotService()
    response = await chatbot_service.generate_response(
        user_message=conversation_data.message,
        conversation_history=conversation.messages
    )
    
    # Update conversation
    from datetime import datetime
    conversation.messages.append({
        "role": "user",
        "content": conversation_data.message,
        "timestamp": datetime.utcnow().isoformat()
    })
    conversation.messages.append({
        "role": "assistant",
        "content": response["message"],
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Update qualification if detected
    if response.get("qualification_detected"):
        conversation.qualification_status = response.get("qualification_status", "pending")
        conversation.qualification_score = response.get("qualification_score", 0.0)
    
    await db.commit()
    await db.refresh(conversation)
    
    return conversation


@router.get("/conversation/{lead_id}", response_model=ConversationResponse)
async def get_conversation(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select
    result = await db.execute(
        select(Conversation).where(
            Conversation.lead_id == lead_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select
    result = await db.execute(
        select(Conversation).where(Conversation.user_id == current_user.id)
    )
    conversations = result.scalars().all()
    
    return conversations

