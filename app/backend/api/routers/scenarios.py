"""Scenarios API Router"""

from fastapi import APIRouter, HTTPException, status

import logging
logger = logging.getLogger(__name__)

router = APIRouter()



@router.post("/generate")
async def generate_scenario(request: dict):
    """
    Generate future urban scenario with Gemini 2.5 Flash
    
    Args:
        request: {source_city, target_policy, user_preferences}
    
    Returns:
        Generated scenario with image and metadata
    """
    logger.info(f"Generating scenario for: {request.get('source_city')}")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Scenario generation not implemented yet"
    )

