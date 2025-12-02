"""
Pricing Router

Handles dynamic pricing calculation endpoints using AI agent.
"""

from fastapi import APIRouter, HTTPException
from models.pricing import PricingRequest, PricingResponse
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


def calculate_confidence_score(
    weather_condition: str,
    time_of_day: str,
    distance_km: float,
    surge_multiplier: float
) -> float:
    """
    Calculate dynamic confidence score based on pricing factors.
    
    Returns a score between 0.60 and 0.95 based on:
    - Weather severity (storms reduce confidence)
    - Time of day (night reduces confidence)
    - Distance (very long trips reduce confidence)
    - Surge multiplier (high volatility reduces confidence)
    
    Args:
        weather_condition: Current weather (clear, rain, storm, etc.)
        time_of_day: Time period (morning, afternoon, evening, night)
        distance_km: Trip distance in kilometers
        surge_multiplier: Current surge pricing multiplier
        
    Returns:
        Confidence score between 0.60 and 0.95
    """
    base_confidence = 0.85  # Start with high confidence
    
    # Reduce confidence for severe weather (more uncertainty)
    if weather_condition:
        weather_lower = weather_condition.lower()
        if any(w in weather_lower for w in ['storm', 'snow', 'heavy']):
            base_confidence -= 0.15
        elif any(w in weather_lower for w in ['rain', 'fog', 'cloud']):
            base_confidence -= 0.08
    
    # Reduce confidence for unusual times (less historical data)
    if time_of_day == 'night':
        base_confidence -= 0.05
    
    # Reduce confidence for very long distances (edge cases)
    if distance_km > 50:
        base_confidence -= 0.10
    elif distance_km > 30:
        base_confidence -= 0.05
    
    # Reduce confidence for high surge (volatile market)
    if surge_multiplier > 2.0:
        base_confidence -= 0.10
    elif surge_multiplier > 1.5:
        base_confidence -= 0.05
    
    # Ensure it stays in valid range (60% to 95%)
    return round(max(0.60, min(0.95, base_confidence)), 2)

router = APIRouter(
    prefix="/api/v1/pricing",
    tags=["pricing"],
    responses={
        200: {"description": "Pricing calculated successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"}
    }
)


@router.post("/calculate", response_model=PricingResponse)
async def calculate_pricing(request: PricingRequest) -> PricingResponse:
    """
    Calculate dynamic pricing for a ride request
    
    This endpoint will integrate with:
    - MongoDB (for historical data and customer info) - Dec 2
    - ChromaDB (for RAG knowledge retrieval) - Dec 3
    - LangChain Agent (for intelligent pricing decisions) - Dec 3
    
    Current implementation: Mock response with simple logic (Dec 1)
    Full AI agent implementation: Dec 3
    
    Args:
        request: PricingRequest containing ride details
        
    Returns:
        PricingResponse with calculated price and reasoning
        
    Raises:
        HTTPException: If pricing calculation fails
    """
    try:
        logger.info(f"Calculating pricing for {request.customer_id}: {request.pickup_location} -> {request.dropoff_location}")
        
        # TODO: Replace with actual agent service call (Dec 3)
        # For now, implement simple mock pricing logic
        
        # Base calculation: $2.50 per km
        base_price = request.distance_km * 2.5
        
        # Time-based surge multiplier
        surge_multiplier = 1.0
        time_surge_map = {
            "morning": 1.3,    # Morning rush: 7-9 AM
            "afternoon": 1.0,  # Regular hours: 12-5 PM
            "evening": 1.5,    # Evening rush: 5-8 PM
            "night": 1.2       # Late night: 8 PM - 2 AM
        }
        surge_multiplier *= time_surge_map.get(request.time_of_day, 1.0)
        
        # Weather-based surge (if provided)
        if request.weather_condition:
            weather_surge_map = {
                "rainy": 1.3,
                "snowy": 1.5,
                "stormy": 1.4,
                "clear": 1.0,
                "cloudy": 1.0
            }
            weather_multiplier = weather_surge_map.get(request.weather_condition.lower(), 1.0)
            surge_multiplier *= weather_multiplier
        
        # Calculate final price
        final_price = base_price * surge_multiplier
        
        # Generate reasoning explanation
        reasoning_parts = [
            f"Base rate: ${base_price:.2f} ({request.distance_km}km × $2.50/km)"
        ]
        
        if surge_multiplier > 1.0:
            if time_surge_map.get(request.time_of_day, 1.0) > 1.0:
                reasoning_parts.append(
                    f"Time surge: {request.time_of_day} hours (×{time_surge_map[request.time_of_day]})"
                )
            
            if request.weather_condition and request.weather_condition.lower() in ["rainy", "snowy", "stormy"]:
                weather_mult = weather_surge_map.get(request.weather_condition.lower(), 1.0)
                reasoning_parts.append(
                    f"Weather impact: {request.weather_condition} conditions (×{weather_mult})"
                )
        else:
            reasoning_parts.append("Standard pricing - low demand period")
        
        reasoning_parts.append(f"Total surge multiplier: ×{surge_multiplier:.2f}")
        
        # Note about mock implementation
        reasoning_parts.append(
            "[MOCK] Full AI agent with RAG knowledge coming Dec 3"
        )
        
        reasoning = ". ".join(reasoning_parts)
        
        # Calculate dynamic confidence score based on conditions
        confidence = calculate_confidence_score(
            weather_condition=request.weather_condition or "clear",
            time_of_day=request.time_of_day,
            distance_km=request.distance_km,
            surge_multiplier=surge_multiplier
        )
        
        response = PricingResponse(
            base_price=round(base_price, 2),
            surge_multiplier=round(surge_multiplier, 2),
            final_price=round(final_price, 2),
            reasoning=reasoning,
            confidence_score=confidence,  # Dynamic confidence based on conditions
            agent_trace_url=None,   # Will be populated with LangSmith URL (Dec 3)
            metadata={
                "customer_id": request.customer_id,
                "implementation": "mock",
                "version": "1.0.0-mock",
                "confidence_factors": {
                    "weather": request.weather_condition or "clear",
                    "time": request.time_of_day,
                    "distance_km": request.distance_km,
                    "surge": surge_multiplier
                }
            }
        )
        
        logger.info(f"Pricing calculated: ${response.final_price:.2f} (surge: {response.surge_multiplier}x)")
        
        return response
        
    except Exception as e:
        logger.error(f"Error calculating pricing: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate pricing: {str(e)}"
        )


@router.get("/history/{customer_id}")
async def get_pricing_history(
    customer_id: str,
    limit: int = 10
) -> Dict:
    """
    Get pricing history for a customer
    
    Implementation: Dec 2 (MongoDB integration)
    
    Args:
        customer_id: Customer identifier
        limit: Maximum number of records to return
        
    Returns:
        Dict containing pricing history
    """
    logger.info(f"Fetching pricing history for customer: {customer_id}")
    
    # TODO: Implement MongoDB query (Dec 2)
    return {
        "customer_id": customer_id,
        "message": "MongoDB integration pending (Dec 2)",
        "mock_data": [],
        "total_rides": 0,
        "average_price": 0.0
    }


@router.get("/factors")
async def get_pricing_factors() -> Dict:
    """
    Get current pricing factors and multipliers
    
    Returns information about what affects pricing calculations.
    
    Returns:
        Dict containing current pricing factors
    """
    return {
        "base_rate_per_km": 2.50,
        "time_multipliers": {
            "morning": 1.3,
            "afternoon": 1.0,
            "evening": 1.5,
            "night": 1.2
        },
        "weather_multipliers": {
            "clear": 1.0,
            "cloudy": 1.0,
            "rainy": 1.3,
            "snowy": 1.5,
            "stormy": 1.4
        },
        "customer_tier_discounts": {
            "bronze": 0.0,
            "silver": 0.05,
            "gold": 0.10,
            "platinum": 0.15
        },
        "note": "Full AI agent with dynamic factors coming Dec 3"
    }


@router.post("/batch", response_model=List[PricingResponse])
async def calculate_batch_pricing(
    requests: List[PricingRequest]
) -> List[PricingResponse]:
    """
    Calculate pricing for multiple ride requests
    
    Useful for comparing routes or times.
    
    Args:
        requests: List of PricingRequest objects
        
    Returns:
        List of PricingResponse objects
        
    Raises:
        HTTPException: If batch processing fails
    """
    try:
        logger.info(f"Processing batch pricing for {len(requests)} requests")
        
        responses = []
        for request in requests:
            response = await calculate_pricing(request)
            responses.append(response)
        
        return responses
        
    except Exception as e:
        logger.error(f"Error in batch pricing: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process batch pricing: {str(e)}"
        )

