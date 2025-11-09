"""Urban Evolution AI Platform - FastAPI Application"""

import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Add project root to path for shared imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import routers with relative imports
from api.routers import buildings, chat, cities, ethics, growth, news, scenarios

# Setup simple logger (middleware will be added later)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Urban Evolution AI Platform...")
    
    # Initialize database
    logger.info("📊 Initializing database...")
    # TODO: Initialize database connection
    
    # Load ML models
    logger.info("🤖 Loading ML models...")
    # TODO: Load YOLO, SAM, LSTM, XGBoost models
    
    # Initialize agent system
    logger.info("🧠 Initializing multi-agent system...")
    # TODO: Initialize LangGraph orchestrator
    
    # Initialize Redis connection
    logger.info("💾 Connecting to Redis...")
    # TODO: Initialize Redis client
    
    logger.info("✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Urban Evolution AI Platform...")
    # TODO: Cleanup resources
    logger.info("✅ Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Urban Evolution AI API",
    description="""
    AI-Powered Urban Evolution Platform combining computer vision, time-series forecasting, 
    multi-agent AI, and generative image editing with Gemini 2.5 Flash.
    
    ## Features
    
    * 🏗️ **Building Detection**: YOLOv11-powered building detection and classification
    * 📈 **Growth Prediction**: LSTM-based spatial urban growth forecasting
    * 🤖 **Multi-Agent System**: LangGraph-orchestrated AI agents for scenario generation
    * 🎨 **Image Editing**: Gemini 2.5 Flash pixel-precise urban transformation
    * 📰 **News Analysis**: Automated extraction of urban development projects
    * ⚖️ **Ethics Guardian**: Bias detection and fairness evaluation
    
    ## Workflow
    
    1. Upload or select city data
    2. Detect and classify buildings
    3. Predict urban growth patterns
    4. Generate future scenarios with policy constraints
    5. Review and approve transformations
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        # Add production origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
# TODO: Implement and enable custom middleware
# app.add_middleware(LoggingMiddleware)
# app.add_middleware(RateLimitMiddleware)
# app.add_middleware(AuthMiddleware)  # Enable after implementing auth

# Include routers
app.include_router(cities.router, prefix="/api/cities", tags=["Cities"])
app.include_router(buildings.router, prefix="/api/buildings", tags=["Buildings"])
app.include_router(growth.router, prefix="/api/growth", tags=["Growth Prediction"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["Scenarios"])
app.include_router(chat.router, prefix="/api/chat", tags=["Multi-Agent Chat"])
app.include_router(news.router, prefix="/api/news", tags=["Urban News"])
app.include_router(ethics.router, prefix="/api/ethics", tags=["Ethics & Safety"])


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint with API information"""
    return {
        "message": "Urban Evolution AI Platform API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "urban-evolution-ai",
    }


# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "status_code": 422,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.exception(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
