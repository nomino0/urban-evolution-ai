"""Multi-Agent Chat API Router"""

from fastapi import APIRouter, HTTPException, status

import logging
logger = logging.getLogger(__name__)

router = APIRouter()



@router.post("/")
async def chat(request: dict):
    """
    Chat with multi-agent system
    
    Args:
        request: {message, conversation_id, city_context}
    
    Returns:
        Agent response with sources and trace
    """
    logger.info(f"Chat request: {request.get('message')[:50]}...")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Multi-agent chat not implemented yet"
    )

