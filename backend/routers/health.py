"""
Health Check Router

Provides health check endpoints for monitoring and diagnostics.
"""

from fastapi import APIRouter
from typing import Dict
from datetime import datetime
from utils.config import settings

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
    - MongoDB (Dec 2 implementation)
    - ChromaDB (Dec 3 implementation)
    - LangChain Agent (Dec 3 implementation)
    
    Returns:
        Dict containing detailed health information for all services
    """
    # TODO: Add actual health checks for dependencies
    # For now, return mock status
    
    services = {
        "api": {
            "status": "operational",
            "version": settings.app_version,
            "environment": settings.environment
        },
        "mongodb": {
            "status": "not_connected",
            "message": "MongoDB integration pending (Dec 2)"
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
    
    # Determine overall status
    overall_status = "healthy"  # Will be "degraded" if any service is down
    
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
    
    Returns:
        Dict indicating if the service is ready to accept traffic
    """
    # TODO: Check if all critical services are ready
    # For now, always return ready
    
    return {
        "status": "ready",
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

