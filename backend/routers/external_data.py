"""
External Data Router

Handles external data endpoints (weather, traffic, events).
"""

from fastapi import APIRouter, HTTPException, Query
from models.external_data import (
    ExternalData,
    ExternalDataCreate,
    ExternalDataSummary,
    WeatherData,
    TrafficData,
    EventData
)
from services.mongodb_service import get_mongodb_service
from typing import List, Optional, Literal
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/external-data",
    tags=["external-data"],
    responses={
        200: {"description": "Operation successful"},
        404: {"description": "Data not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get("/", response_model=List[ExternalData])
async def list_external_data(
    data_type: Optional[Literal["weather", "traffic", "events"]] = Query(
        None,
        description="Filter by data type"
    ),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(default=10, ge=1, le=100)
) -> List[ExternalData]:
    """
    List external data with optional filtering
    
    Only returns non-expired data (ttl > now).
    
    Args:
        data_type: Filter by data type (weather, traffic, events)
        location: Filter by location
        limit: Maximum number of records to return (1-100)
        
    Returns:
        List of ExternalData objects
    """
    logger.info(f"Listing external data (type={data_type}, location={location}, limit={limit})")
    
    try:
        db_service = get_mongodb_service()
        data = await db_service.get_external_data(data_type, location, limit)
        
        return [ExternalData(**item) for item in data]
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error listing external data: {e}")
        return []


@router.get("/weather/{location}", response_model=Optional[ExternalData])
async def get_weather(location: str):
    """
    Get latest weather data for a location
    
    Args:
        location: Location/zone (e.g., Urban, Suburban)
        
    Returns:
        Latest weather ExternalData or None
    """
    logger.info(f"Fetching weather for location: {location}")
    
    try:
        db_service = get_mongodb_service()
        data = await db_service.get_weather_data(location)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No weather data found for location: {location}"
            )
        
        return ExternalData(**data)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch weather data: {str(e)}"
        )


@router.get("/traffic/{location}", response_model=Optional[ExternalData])
async def get_traffic(location: str):
    """
    Get latest traffic data for a location
    
    Args:
        location: Location/zone (e.g., Urban, Suburban)
        
    Returns:
        Latest traffic ExternalData or None
    """
    logger.info(f"Fetching traffic for location: {location}")
    
    try:
        db_service = get_mongodb_service()
        data = await db_service.get_traffic_data(location)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No traffic data found for location: {location}"
            )
        
        return ExternalData(**data)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching traffic: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch traffic data: {str(e)}"
        )


@router.get("/events/{location}", response_model=Optional[ExternalData])
async def get_events(location: str):
    """
    Get latest events data for a location
    
    Args:
        location: Location/zone (e.g., Urban, Suburban)
        
    Returns:
        Latest events ExternalData or None
    """
    logger.info(f"Fetching events for location: {location}")
    
    try:
        db_service = get_mongodb_service()
        data = await db_service.get_events_data(location)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No events data found for location: {location}"
            )
        
        return ExternalData(**data)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch events data: {str(e)}"
        )


@router.post("/", response_model=ExternalData, status_code=201)
async def create_external_data(data: ExternalDataCreate) -> ExternalData:
    """
    Create new external data record
    
    Automatically sets timestamp to now and TTL to 6 hours from now if not provided.
    
    Args:
        data: ExternalDataCreate object
        
    Returns:
        Created ExternalData object
        
    Raises:
        HTTPException: If creation fails
    """
    logger.info(f"Creating external data: {data.data_type} for {data.location}")
    
    try:
        db_service = get_mongodb_service()
        
        # Convert to dict
        data_dict = data.model_dump()
        
        # Create the record
        await db_service.create_external_data(data_dict)
        
        logger.info(f"✅ External data created: {data.data_type} for {data.location}")
        
        # Fetch and return the created data
        created_data = await db_service.get_latest_external_data(data.data_type, data.location)
        return ExternalData(**created_data)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except Exception as e:
        logger.error(f"Error creating external data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create external data: {str(e)}"
        )


@router.get("/summary", response_model=List[ExternalDataSummary])
async def get_external_data_summary() -> List[ExternalDataSummary]:
    """
    Get summary of external data by type and location
    
    Shows record counts and latest timestamps for each data type/location combination.
    Only includes non-expired data.
    
    Returns:
        List of ExternalDataSummary objects
    """
    logger.info("Fetching external data summary")
    
    try:
        db_service = get_mongodb_service()
        summary = await db_service.get_external_data_summary()
        
        return [ExternalDataSummary(**item) for item in summary]
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error fetching summary: {e}")
        return []


@router.delete("/cleanup", status_code=200)
async def cleanup_expired_data():
    """
    Clean up expired external data
    
    Removes all records where ttl <= current time.
    This endpoint can be called periodically to maintain the database.
    
    Returns:
        Dict with number of records deleted
    """
    logger.info("Cleaning up expired external data")
    
    try:
        db_service = get_mongodb_service()
        deleted_count = await db_service.cleanup_expired_external_data()
        
        return {
            "status": "success",
            "deleted_count": deleted_count,
            "message": f"Deleted {deleted_count} expired records"
        }
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except Exception as e:
        logger.error(f"Error cleaning up expired data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup expired data: {str(e)}"
        )

