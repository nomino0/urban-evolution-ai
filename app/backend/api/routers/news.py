"""Urban News API Router"""

from fastapi import APIRouter, HTTPException, status

import logging
logger = logging.getLogger(__name__)

router = APIRouter()



@router.get("/{city_name}")
async def get_news(city_name: str):
    """
    Get urban development news for a city
    
    Args:
        city_name: Name of the city
    
    Returns:
        List of news articles with extracted projects
    """
    logger.info(f"Fetching news for: {city_name}")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="News scraping not implemented yet"
    )

