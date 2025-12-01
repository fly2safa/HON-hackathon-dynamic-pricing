"""
Rides Router

Handles ride management endpoints (CRUD operations).
"""

from fastapi import APIRouter, HTTPException, Query
from models.ride import RideRequest, RideResponse, RideHistoryItem
from services.mongodb_service import get_mongodb_service
from typing import List
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/rides",
    tags=["rides"],
    responses={
        200: {"description": "Operation successful"},
        404: {"description": "Ride not found"},
        500: {"description": "Internal server error"}
    }
)


@router.post("/", response_model=RideResponse, status_code=201)
async def create_ride(ride: RideRequest) -> RideResponse:
    """
    Create a new ride record with MongoDB storage
    
    This endpoint creates a ride record with pricing calculation and saves it to MongoDB.
    
    Args:
        ride: RideRequest containing ride details
        
    Returns:
        RideResponse with ride details and pricing
        
    Raises:
        HTTPException: If ride creation fails
    """
    try:
        logger.info(f"Creating ride for customer {ride.customer_id}")
        
        # Generate unique ride ID
        ride_id = f"RIDE_{uuid.uuid4().hex[:8].upper()}"
        
        # TODO: Replace with actual pricing agent service call (Dec 3)
        # For now, use simple mock pricing
        base_price = ride.distance_km * 2.5
        
        # Simple time-based surge
        surge_multiplier = 1.0
        if ride.time_of_day in ["morning", "evening"]:
            surge_multiplier = 1.5
        elif ride.time_of_day == "night":
            surge_multiplier = 1.2
        
        final_price = base_price * surge_multiplier
        
        # Create pricing decision data (matches pricing_decisions collection schema)
        pricing_decision_data = {
            "ride_id": ride_id,
            "calculated_price": round(final_price, 2),
            "base_price": round(base_price, 2),
            "surge_multiplier": surge_multiplier,
            "reasoning": {
                "method": "mock",
                "factors": {
                    "time_of_day": ride.time_of_day,
                    "weather": ride.weather_condition,
                    "base_rate_per_km": 2.5
                },
                "explanation": f"Ride at {ride.time_of_day}, {ride.distance_km}km. Mock pricing (AI agent coming Dec 3)."
            },
            "agent_trace": [],
            "applied": False,
            "customer_id": ride.customer_id,
            "pickup_location": ride.pickup_location,
            "dropoff_location": ride.dropoff_location,
            "distance_km": ride.distance_km,
            "time_of_day": ride.time_of_day,
            "weather_condition": ride.weather_condition,
            "confidence_score": 0.75
        }
        
        # Save to MongoDB (pricing_decisions collection)
        try:
            db_service = get_mongodb_service()
            await db_service.create_pricing_decision(pricing_decision_data)
            logger.info(f"✅ Pricing decision saved to MongoDB: {ride_id} - ${final_price:.2f}")
        except RuntimeError as db_error:
            logger.warning(f"⚠️  MongoDB not available: {db_error}. Returning pricing without persistence.")
        except Exception as db_error:
            logger.error(f"❌ MongoDB save failed: {db_error}. Returning pricing without persistence.")
        
        # Convert to RideResponse format for API response
        response_data = {
            "ride_id": ride_id,
            "pickup_location": ride.pickup_location,
            "dropoff_location": ride.dropoff_location,
            "distance_km": ride.distance_km,
            "customer_id": ride.customer_id,
            "base_price": round(base_price, 2),
            "surge_multiplier": surge_multiplier,
            "final_price": round(final_price, 2),
            "reasoning": pricing_decision_data["reasoning"]["explanation"],
            "confidence_score": 0.75,
            "created_at": datetime.now()
        }
        response = RideResponse(**response_data)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating ride: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create ride: {str(e)}"
        )


@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(ride_id: str) -> RideResponse:
    """
    Get pricing decision by ID from MongoDB
    
    Args:
        ride_id: Unique ride identifier
        
    Returns:
        RideResponse with pricing details
        
    Raises:
        HTTPException: If ride not found or query fails
    """
    logger.info(f"Fetching pricing decision: {ride_id}")
    
    try:
        db_service = get_mongodb_service()
        pricing_data = await db_service.get_pricing_decision(ride_id)
        
        if not pricing_data:
            raise HTTPException(
                status_code=404,
                detail=f"Pricing decision not found: {ride_id}"
            )
        
        # Convert pricing_decision format to RideResponse format
        response_data = {
            "ride_id": pricing_data.get("ride_id"),
            "pickup_location": pricing_data.get("pickup_location", ""),
            "dropoff_location": pricing_data.get("dropoff_location", ""),
            "distance_km": pricing_data.get("distance_km", 0),
            "customer_id": pricing_data.get("customer_id", ""),
            "base_price": pricing_data.get("base_price", 0),
            "surge_multiplier": pricing_data.get("surge_multiplier", 1.0),
            "final_price": pricing_data.get("calculated_price", 0),
            "reasoning": pricing_data.get("reasoning", {}).get("explanation", "No reasoning available") if isinstance(pricing_data.get("reasoning"), dict) else str(pricing_data.get("reasoning", "")),
            "confidence_score": pricing_data.get("confidence_score", 0.5),
            "created_at": pricing_data.get("timestamp", datetime.now())
        }
        
        return RideResponse(**response_data)
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching pricing decision: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch pricing decision: {str(e)}"
        )


@router.get("/customer/{customer_id}", response_model=List[RideHistoryItem])
async def get_customer_rides(
    customer_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0)
) -> List[RideHistoryItem]:
    """
    Get all rides for a specific customer from MongoDB
    
    Args:
        customer_id: Customer identifier
        limit: Maximum number of rides to return (1-100)
        skip: Number of rides to skip (for pagination)
        
    Returns:
        List of RideHistoryItem objects
    """
    logger.info(f"Fetching rides for customer: {customer_id} (limit={limit}, skip={skip})")
    
    try:
        db_service = get_mongodb_service()
        rides = await db_service.get_customer_rides(customer_id, limit, skip)
        
        return [RideHistoryItem(**ride) for ride in rides]
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error fetching customer rides: {e}")
        return []


@router.get("/", response_model=List[RideHistoryItem])
async def list_rides(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0)
) -> List[RideHistoryItem]:
    """
    List all rides (with pagination) from MongoDB
    
    Args:
        limit: Maximum number of rides to return (1-100)
        skip: Number of rides to skip (for pagination)
        
    Returns:
        List of RideHistoryItem objects
    """
    logger.info(f"Listing rides (limit={limit}, skip={skip})")
    
    try:
        db_service = get_mongodb_service()
        rides = await db_service.get_rides(limit, skip)
        
        return [RideHistoryItem(**ride) for ride in rides]
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error listing rides: {e}")
        return []


@router.delete("/{ride_id}", status_code=204)
async def delete_ride(ride_id: str):
    """
    Delete a ride by ID from MongoDB
    
    Args:
        ride_id: Unique ride identifier
        
    Raises:
        HTTPException: If ride not found or deletion fails
    """
    logger.info(f"Deleting ride: {ride_id}")
    
    try:
        db_service = get_mongodb_service()
        deleted = await db_service.delete_ride(ride_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Ride not found: {ride_id}"
            )
        
        logger.info(f"✅ Ride deleted: {ride_id}")
        return None
        
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Database service not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting ride: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete ride: {str(e)}"
        )


@router.get("/stats/summary")
async def get_ride_stats():
    """
    Get pricing statistics summary using MongoDB aggregation
    
    Returns:
        Dict containing pricing statistics from pricing_decisions collection
    """
    logger.info("Fetching pricing statistics")
    
    try:
        db_service = get_mongodb_service()
        stats = await db_service.get_ride_statistics()
        
        logger.info(f"✅ Statistics: {stats.get('total_pricing_decisions', 0)} decisions, ${stats.get('total_revenue', 0)} revenue")
        return stats
        
    except RuntimeError:
        logger.warning("⚠️  MongoDB not available")
        return {
            "total_pricing_decisions": 0,
            "total_revenue": 0.0,
            "average_price": 0.0,
            "average_base_price": 0.0,
            "average_surge_multiplier": 0.0,
            "average_distance": 0.0,
            "message": "Database service not available"
        }
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return {
            "total_pricing_decisions": 0,
            "total_revenue": 0.0,
            "average_price": 0.0,
            "average_base_price": 0.0,
            "average_surge_multiplier": 0.0,
            "average_distance": 0.0,
            "error": str(e)
        }

