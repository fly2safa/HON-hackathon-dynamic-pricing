"""
HoneyGo Dynamic Pricing API - Main Application

FastAPI backend for intelligent ride-sharing pricing using LangChain agents and RAG.

Author: Dari (Role 3 - Backend/FastAPI Engineer)
Created: Dec 1, 2024
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.config import settings
from services import mongodb_service as mongo_module
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Agentic AI for ride-sharing dynamic pricing with RAG and observability",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    
    # Initialize MongoDB connection
    try:
        logger.info("🔗 Connecting to MongoDB...")
        mongo_module.mongodb_service = mongo_module.MongoDBService(settings.mongodb_uri)
        await mongo_module.mongodb_service.connect()
        logger.info("✅ MongoDB connected and ready")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        logger.warning("⚠️  API will run in degraded mode (without database persistence)")
        mongo_module.mongodb_service = None
    
    # TODO: Initialize other services (Dec 3)
    # - ChromaDB connection
    # - LangChain agent initialization


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down HoneyGo API")
    
    # Close MongoDB connection
    if mongo_module.mongodb_service:
        try:
            await mongo_module.mongodb_service.disconnect()
            logger.info("✅ MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
    
    # TODO: Close other connections (Dec 3)


@app.get("/")
async def root():
    """
    Root endpoint - API welcome message
    
    Returns basic information about the API.
    """
    return {
        "message": "Welcome to HoneyGo Dynamic Pricing API",
        "version": settings.app_version,
        "status": "operational",
        "docs": f"{settings.backend_url}/docs",
        "description": "Intelligent ride-sharing pricing with AI agents"
    }


@app.get("/health")
async def health_check():
    """
    Basic health check endpoint
    
    Returns the health status of the API.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


# Import and include routers
from routers import health, pricing, rides, drivers, external_data

app.include_router(health.router)
app.include_router(pricing.router)
app.include_router(rides.router)
app.include_router(drivers.router)
app.include_router(external_data.router)


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on port {settings.backend_port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level
    )

