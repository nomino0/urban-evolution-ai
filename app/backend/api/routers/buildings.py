"""Buildings API Router"""

from fastapi import APIRouter, HTTPException, status

import logging
logger = logging.getLogger(__name__)

router = APIRouter()



@router.get("/{city_name}")
async def get_buildings(city_name: str):
    """
    Get buildings detected in a city
    
    Args:
        city_name: Name of the city
    
    Returns:
        List of buildings with geometries and classifications
    """
    logger.info(f"Fetching buildings for city: {city_name}")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Building detection not implemented yet"
    )

