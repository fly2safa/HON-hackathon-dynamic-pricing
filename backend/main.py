"""
HoneyGo Dynamic Pricing API - Main Application

FastAPI backend for intelligent ride-sharing pricing using LangChain agents and RAG.

Author: Dari (Role 3 - Backend/FastAPI Engineer)
Created: Dec 1, 2024
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.config import settings
from services import mongodb_service as mongo_module
from services import chromadb_service as chroma_module
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events.
    Replaces deprecated @app.on_event decorators.
    """
    # Startup
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
    
    # Initialize ChromaDB connection
    try:
        logger.info("🔗 Connecting to ChromaDB...")
        await chroma_module.init_chromadb_service(
            persist_directory=settings.chroma_persist_directory
        )
        stats = chroma_module.chromadb_service.get_stats()
        logger.info(f"✅ ChromaDB connected - Collections: {stats.get('collections', {})}")
    except Exception as e:
        logger.error(f"❌ ChromaDB connection failed: {e}")
        logger.warning("⚠️  RAG queries will be unavailable")
        chroma_module.chromadb_service = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down HoneyGo API")
    
    # Close MongoDB connection
    if mongo_module.mongodb_service:
        try:
            await mongo_module.mongodb_service.disconnect()
            logger.info("✅ MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
    
    # Close ChromaDB connection
    if chroma_module.chromadb_service:
        try:
            await chroma_module.chromadb_service.disconnect()
            logger.info("✅ ChromaDB connection closed")
        except Exception as e:
            logger.error(f"Error closing ChromaDB connection: {e}")


# Create FastAPI application with lifespan handler
app = FastAPI(
    title=settings.app_name,
    description="Agentic AI for ride-sharing dynamic pricing with RAG and observability",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
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
from routers import health, pricing, rides, drivers, external_data, n8n, chat

app.include_router(health.router)
app.include_router(pricing.router)
app.include_router(rides.router)
app.include_router(drivers.router)
app.include_router(external_data.router)
app.include_router(n8n.router)
app.include_router(chat.router)


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

