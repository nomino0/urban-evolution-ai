"""Cities API Router"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# TODO: from app.backend.database.models import City
import logging
logger = logging.getLogger(__name__)

router = APIRouter()



# Dependency for database session (to be implemented)
def get_db():
    """Get database session"""
    # TODO: Implement database session
    pass


@router.get("/", response_model=List[dict])
async def list_cities(db: Session = Depends(get_db)):
    """
    List all available cities
    
    Returns list of cities with basic information
    """
    logger.info("Fetching all cities")
    # TODO: Implement city listing
    return [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Tunis",
            "country": "Tunisia",
            "population": 2700000,
            "area_km2": 212.63,
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "name": "Copenhagen",
            "country": "Denmark",
            "population": 1346000,
            "area_km2": 179.8,
        },
    ]


@router.get("/{city_id}", response_model=dict)
async def get_city(city_id: UUID, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific city
    
    Args:
        city_id: City UUID
    
    Returns:
        City details including boundaries, demographics, and available data
    """
    logger.info(f"Fetching city: {city_id}")
    # TODO: Implement city retrieval
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet"
    )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_city(city_data: dict, db: Session = Depends(get_db)):
    """
    Create a new city entry
    
    Args:
        city_data: City information including name, country, boundaries
    
    Returns:
        Created city object
    """
    logger.info(f"Creating new city: {city_data.get('name')}")
    # TODO: Implement city creation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet"
    )

