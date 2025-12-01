"""
Health Check Router

Provides health check endpoints for monitoring and diagnostics.
"""

from fastapi import APIRouter
from typing import Dict
from datetime import datetime
from utils.config import settings
from services import mongodb_service

router = APIRouter(
    prefix="/api/v1/health",
    tags=["health"],
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"}
    }
)


@router.get("/")
async def health_check() -> Dict[str, str]:
    """
    Basic health check endpoint
    
    Returns:
        Dict containing health status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HoneyGo API"
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict:
    """
    Detailed health check with dependency status
    
    Checks connectivity to:
    - MongoDB (IMPLEMENTED)
    - ChromaDB (Dec 3 implementation)
    - LangChain Agent (Dec 3 implementation)
    
    Returns:
        Dict containing detailed health information for all services
    """
    # Check MongoDB connection status
    mongodb_status = "not_connected"
    mongodb_message = "MongoDB not initialized"
    
    if mongodb_service.mongodb_service:
        if mongodb_service.mongodb_service.connected:
            mongodb_status = "connected"
            mongodb_message = f"Connected to database: {mongodb_service.mongodb_service.db.name}"
            
            # Try to ping the database
            try:
                mongodb_service.mongodb_service.client.admin.command('ping')
                mongodb_message += " (ping successful)"
            except Exception as e:
                mongodb_status = "degraded"
                mongodb_message = f"Connected but ping failed: {str(e)}"
        else:
            mongodb_status = "disconnected"
            mongodb_message = "MongoDB service initialized but not connected"
    
    services = {
        "api": {
            "status": "operational",
            "version": settings.app_version,
            "environment": settings.environment
        },
        "mongodb": {
            "status": mongodb_status,
            "message": mongodb_message,
            "database": mongodb_service.mongodb_service.db.name if mongodb_service.mongodb_service and mongodb_service.mongodb_service.connected else "N/A"
        },
        "chromadb": {
            "status": "not_connected",
            "message": "ChromaDB integration pending (Dec 3)"
        },
        "langchain_agent": {
            "status": "not_configured",
            "message": "LangChain agent integration pending (Dec 3)"
        }
    }
    
    # Determine overall status based on critical services
    if mongodb_status == "connected":
        overall_status = "healthy"
    elif mongodb_status in ["degraded", "disconnected"]:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "services": services,
        "version": settings.app_version
    }


@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check for Kubernetes/container orchestration
    
    Service is ready if critical services (MongoDB) are available.
    
    Returns:
        Dict indicating if the service is ready to accept traffic
    """
    # Check if MongoDB is connected (critical service)
    is_ready = False
    status = "not_ready"
    
    if mongodb_service.mongodb_service and mongodb_service.mongodb_service.connected:
        try:
            # Test MongoDB connection with a ping
            mongodb_service.mongodb_service.client.admin.command('ping')
            is_ready = True
            status = "ready"
        except Exception:
            status = "not_ready"
            is_ready = False
    
    return {
        "status": status,
        "ready": is_ready,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes/container orchestration
    
    Returns:
        Dict indicating if the service is alive (running)
    """
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat()
    }

