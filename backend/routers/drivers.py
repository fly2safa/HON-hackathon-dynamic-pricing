"""
Drivers Router

Handles driver management endpoints (CRUD operations and statistics).
"""

from fastapi import APIRouter, HTTPException, Query
from models.driver import Driver, DriverCreate, DriverUpdate, DriverStats
from services.mongodb_service import get_mongodb_service
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/drivers",
    tags=["drivers"],
    responses={
        200: {"description": "Operation successful"},
        404: {"description": "Driver not found"},
        500: {"description": "Internal server error"}
    }
)


@router.get("/", response_model=List[Driver])
async def list_drivers(
    status: Optional[str] = Query(None, description="Filter by status (e.g., Active)"),
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0)
) -> List[Driver]:
    """
    List all drivers with optional filtering
    
    Args:
        status: Filter by driver status (Active, Inactive)
        limit: Maximum number of drivers to return (1-100)
        skip: Number of drivers to skip (for pagination)
        
    Returns:
        List of Driver objects
    """
    logger.info(f"Listing drivers (status={status}, limit={limit}, skip={skip})")
    
    try:
        db_service = get_mongodb_service()
        
        # Build filter query
        filter_query = {}
        if status:
            filter_query["status"] = status
        
        drivers = await db_service.get_drivers(limit, skip, filter_query)
        
        return [Driver(**driver) for driver in drivers]
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error listing drivers: {e}")
        return []


@router.get("/active", response_model=List[Driver])
async def list_active_drivers(
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(default=20, ge=1, le=100)
) -> List[Driver]:
    """
    List active drivers, optionally filtered by location
    
    Args:
        location: Filter by current location (e.g., Urban, Suburban)
        limit: Maximum number of drivers to return
        
    Returns:
        List of active Driver objects sorted by rating
    """
    logger.info(f"Listing active drivers (location={location}, limit={limit})")
    
    try:
        db_service = get_mongodb_service()
        drivers = await db_service.get_active_drivers(location, limit)
        
        return [Driver(**driver) for driver in drivers]
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error listing active drivers: {e}")
        return []


@router.get("/stats/summary")
async def get_driver_statistics():
    """
    Get driver statistics summary
    
    Returns aggregate statistics for all drivers including:
    - Total drivers
    - Active drivers
    - Total rides completed
    - Total earnings
    - Average rating
    
    Returns:
        Dict containing driver statistics
    """
    logger.info("Fetching driver statistics")
    
    try:
        db_service = get_mongodb_service()
        stats = await db_service.get_driver_statistics()
        
        logger.info(f"✅ Statistics: {stats.get('total_drivers', 0)} drivers, {stats.get('active_drivers', 0)} active")
        return stats
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available")
        return {
            "total_drivers": 0,
            "active_drivers": 0,
            "total_rides_completed": 0,
            "total_earnings": 0.0,
            "average_rating": 0.0,
            "average_earnings_per_driver": 0.0,
            "message": "Database service not available"
        }
    except Exception as e:
        logger.error(f"Error fetching driver statistics: {e}")
        return {
            "total_drivers": 0,
            "active_drivers": 0,
            "total_rides_completed": 0,
            "total_earnings": 0.0,
            "average_rating": 0.0,
            "average_earnings_per_driver": 0.0,
            "error": str(e)
        }


@router.get("/{driver_id}", response_model=Driver)
async def get_driver(driver_id: str) -> Driver:
    """
    Get driver details by ID
    
    Args:
        driver_id: Unique driver identifier
        
    Returns:
        Driver object with full details
        
    Raises:
        HTTPException: If driver not found or query fails
    """
    logger.info(f"Fetching driver: {driver_id}")
    
    try:
        db_service = get_mongodb_service()
        driver_data = await db_service.get_driver(driver_id)
        
        if not driver_data:
            raise HTTPException(
                status_code=404,
                detail=f"Driver not found: {driver_id}"
            )
        
        return Driver(**driver_data)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching driver: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch driver: {str(e)}"
        )


@router.post("/", response_model=Driver, status_code=201)
async def create_driver(driver: DriverCreate) -> Driver:
    """
    Create a new driver
    
    Args:
        driver: DriverCreate data
        
    Returns:
        Created Driver object
        
    Raises:
        HTTPException: If creation fails
    """
    logger.info(f"Creating driver: {driver.driver_id}")
    
    try:
        db_service = get_mongodb_service()
        
        # Convert to dict and add defaults
        driver_data = driver.model_dump()
        driver_data["total_rides_completed"] = 0
        driver_data["total_earnings"] = 0.0
        driver_data["rating"] = 0.0
        driver_data["availability"] = {}
        driver_data["earnings_stats"] = {}
        driver_data["incentives"] = {}
        driver_data["performance_metrics"] = {}
        
        await db_service.create_driver(driver_data)
        
        logger.info(f"✅ Driver created: {driver.driver_id}")
        
        # Fetch and return the created driver
        created_driver = await db_service.get_driver(driver.driver_id)
        return Driver(**created_driver)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except Exception as e:
        logger.error(f"Error creating driver: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create driver: {str(e)}"
        )


@router.patch("/{driver_id}", response_model=Driver)
async def update_driver(driver_id: str, update: DriverUpdate) -> Driver:
    """
    Update driver information
    
    Args:
        driver_id: Unique driver identifier
        update: DriverUpdate data with fields to update
        
    Returns:
        Updated Driver object
        
    Raises:
        HTTPException: If driver not found or update fails
    """
    logger.info(f"Updating driver: {driver_id}")
    
    try:
        db_service = get_mongodb_service()
        
        # Convert to dict, excluding None values
        update_data = update.model_dump(exclude_none=True)
        
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )
        
        success = await db_service.update_driver(driver_id, update_data)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Driver not found: {driver_id}"
            )
        
        logger.info(f"✅ Driver updated: {driver_id}")
        
        # Fetch and return the updated driver
        updated_driver = await db_service.get_driver(driver_id)
        return Driver(**updated_driver)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating driver: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update driver: {str(e)}"
        )

