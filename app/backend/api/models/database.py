"""SQLAlchemy Database Models"""

import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


# =============================================================================
# Enums
# =============================================================================


class TileStatus(str, enum.Enum):
    """Tile download status"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    ALIGNMENT_ERROR = "alignment_error"


class BuildingType(str, enum.Enum):
    """Building classification types"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    GOVERNMENT = "government"
    OTHER = "other"


# =============================================================================
# Models
# =============================================================================


class City(Base):
    """City model with geographic boundaries"""
    
    __tablename__ = "cities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=False)
    
    # Geographic boundaries (GeoJSON-like structure)
    master_bbox = Column(JSON, nullable=False)  # {west, south, east, north}
    expansion_zone_bbox = Column(JSON, nullable=True)
    
    # Demographics
    population = Column(Integer, nullable=True)
    area_km2 = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    tiles = relationship("Tile", back_populates="city", cascade="all, delete-orphan")
    buildings = relationship("Building", back_populates="city", cascade="all, delete-orphan")
    growth_predictions = relationship("GrowthPrediction", back_populates="city", cascade="all, delete-orphan")
    scenarios = relationship("Scenario", back_populates="source_city", cascade="all, delete-orphan")
    news_cache = relationship("NewsCache", back_populates="city", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, country={self.country})>"


class Tile(Base):
    """Data tile model for aligned multi-source imagery"""
    
    __tablename__ = "tiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False, index=True)
    
    # Tile identification
    tile_id = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "tunis_tile_05_03"
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    
    # Geographic extent
    bbox = Column(JSON, nullable=False)  # {west, south, east, north}
    zoom_level = Column(Integer, nullable=False, default=14)
    
    # Processing status
    status = Column(Enum(TileStatus), default=TileStatus.PENDING, nullable=False, index=True)
    alignment_verified = Column(Boolean, default=False, nullable=False)
    
    # Data sources (paths to files)
    data_sources = Column(JSON, nullable=True)  # {sentinel2, osm_buildings, osm_render, topographic}
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    city = relationship("City", back_populates="tiles")
    buildings = relationship("Building", back_populates="tile", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tile(id={self.id}, tile_id={self.tile_id}, status={self.status})>"


class Building(Base):
    """Building detection and classification model"""
    
    __tablename__ = "buildings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False, index=True)
    tile_id = Column(UUID(as_uuid=True), ForeignKey("tiles.id"), nullable=True, index=True)
    
    # Geometry (GeoJSON format)
    geometry = Column(JSON, nullable=False)  # Polygon coordinates
    
    # Classification
    building_type = Column(Enum(BuildingType), nullable=True, index=True)
    building_type_confidence = Column(Float, nullable=True)
    
    # Physical characteristics
    height_meters = Column(Float, nullable=True)  # Actual height if known
    estimated_height = Column(Float, nullable=True)  # Shadow-based estimate
    num_floors = Column(Integer, nullable=True)
    building_area_sqm = Column(Float, nullable=True)
    
    # Capacity estimation
    capacity_people = Column(Integer, nullable=True)
    capacity_workers = Column(Integer, nullable=True)
    
    # Detection metadata
    year_detected = Column(Integer, nullable=False)
    detection_confidence = Column(Float, nullable=True)
    detection_model = Column(String(50), default="yolov11", nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    city = relationship("City", back_populates="buildings")
    tile = relationship("Tile", back_populates="buildings")
    
    def __repr__(self):
        return f"<Building(id={self.id}, type={self.building_type}, height={self.estimated_height}m)>"


class GrowthPrediction(Base):
    """Urban growth prediction model"""
    
    __tablename__ = "growth_predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False, index=True)
    
    # Prediction parameters
    target_year = Column(Integer, nullable=False, index=True)
    base_year = Column(Integer, nullable=False, default=2024)
    
    # Outputs
    heatmap_path = Column(String(500), nullable=True)  # Path to GeoTIFF
    heatmap_geojson = Column(JSON, nullable=True)  # GeoJSON polygons
    
    # Population forecast
    population_forecast = Column(Integer, nullable=True)
    confidence_interval_low = Column(Integer, nullable=True)
    confidence_interval_high = Column(Integer, nullable=True)
    
    # News-based adjustments
    announced_projects = Column(JSON, nullable=True)  # Array of projects
    news_analysis_date = Column(DateTime(timezone=True), nullable=True)
    
    # Model information
    model_version = Column(String(50), nullable=True)
    prediction_confidence = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    city = relationship("City", back_populates="growth_predictions")
    
    def __repr__(self):
        return f"<GrowthPrediction(city={self.city_id}, year={self.target_year}, pop={self.population_forecast})>"


class Scenario(Base):
    """Generated urban scenario model"""
    
    __tablename__ = "scenarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    source_city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False, index=True)
    
    # Policy and reference
    target_policy = Column(String(100), nullable=False, index=True)  # e.g., "EU_GREEN_CITIES"
    reference_city = Column(String(100), nullable=True)
    
    # Generation inputs
    prompt = Column(Text, nullable=False)
    tile_id = Column(String(100), nullable=True)
    edit_regions = Column(JSON, nullable=False)  # Array of edit region specifications
    
    # Generation outputs
    image_path = Column(String(500), nullable=True)
    generation_status = Column(String(50), default="pending", nullable=False)
    
    # Cost tracking
    generation_cost = Column(Float, nullable=True)
    api_provider = Column(String(50), default="gemini_2.5_flash", nullable=True)
    
    # User preferences
    user_preferences = Column(JSON, nullable=True)
    
    # Ethics review
    ethics_score = Column(Float, nullable=True)
    ethics_review = Column(JSON, nullable=True)
    human_approved = Column(Boolean, default=False, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    source_city = relationship("City", back_populates="scenarios")
    
    def __repr__(self):
        return f"<Scenario(id={self.id}, policy={self.target_policy}, cost=${self.generation_cost})>"


class NewsCache(Base):
    """Cached urban development news"""
    
    __tablename__ = "news_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False, index=True)
    
    # Article information
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    url = Column(String(1000), nullable=False)
    source = Column(String(200), nullable=True)
    
    # Sentiment analysis
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    
    # Extracted projects
    projects_extracted = Column(JSON, nullable=True)  # Array of project objects
    
    # Timestamps
    published_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    city = relationship("City", back_populates="news_cache")
    
    def __repr__(self):
        return f"<NewsCache(id={self.id}, title={self.title[:50]}...)>"
