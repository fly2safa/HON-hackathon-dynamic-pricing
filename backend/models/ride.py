"""
Ride Data Models

Pydantic models for ride-related data validation and serialization.
Adapted to match existing MongoDB schema from CSV data.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class HistoricalRide(BaseModel):
    """
    Model for historical ride data from CSV (rides collection)
    
    This matches the existing MongoDB schema from imported CSV data.
    """
    number_of_riders: Optional[int] = Field(None, description="Number of riders")
    number_of_drivers: Optional[int] = Field(None, description="Number of available drivers")
    location_category: Optional[str] = Field(None, description="Location category (Urban, Suburban, etc.)")
    customer_loyalty_status: Optional[str] = Field(None, description="Customer loyalty tier")
    number_of_past_rides: Optional[int] = Field(None, description="Customer's past rides")
    average_ratings: Optional[float] = Field(None, description="Customer rating")
    time_of_booking: Optional[str] = Field(None, description="Time of booking")
    vehicle_type: Optional[str] = Field(None, description="Vehicle type")
    expected_ride_duration: Optional[int] = Field(None, description="Expected duration in minutes")
    historical_cost_of_ride: Optional[float] = Field(None, description="Historical cost from CSV")
    timestamp: Optional[datetime] = Field(None, description="Record timestamp")
    enriched_data: Optional[Dict[str, Any]] = Field(None, description="Additional enriched data")
    
    class Config:
        from_attributes = True


class RideBase(BaseModel):
    """Base ride model with common fields for new ride requests"""
    pickup_location: str = Field(..., description="Starting location for the ride")
    dropoff_location: str = Field(..., description="Destination location")
    distance_km: float = Field(..., gt=0, description="Distance in kilometers")
    customer_id: str = Field(..., description="Customer identifier")


class RideRequest(RideBase):
    """
    Ride request model for creating new rides
    
    Extends RideBase with additional fields needed for pricing calculations.
    """
    time_of_day: str = Field(
        default="afternoon",
        description="Time of day: morning, afternoon, evening, or night"
    )
    weather_condition: Optional[str] = Field(
        None,
        description="Current weather condition (optional)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "pickup_location": "Downtown Charlotte",
                "dropoff_location": "Charlotte Douglas Airport",
                "distance_km": 15.5,
                "customer_id": "CUST_0042",
                "time_of_day": "evening",
                "weather_condition": "rainy"
            }
        }


class RideResponse(BaseModel):
    """
    Ride response model with pricing information
    
    Returned after a ride is created with calculated pricing.
    """
    ride_id: str = Field(..., description="Unique ride identifier")
    pickup_location: str
    dropoff_location: str
    distance_km: float
    customer_id: str
    base_price: float = Field(..., description="Base price before surge")
    surge_multiplier: float = Field(..., description="Surge pricing multiplier")
    final_price: float = Field(..., description="Final calculated price")
    reasoning: str = Field(..., description="AI agent's pricing reasoning")
    confidence_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Agent's confidence in the pricing decision (0-1)"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "ride_id": "RIDE_001",
                "pickup_location": "Downtown Charlotte",
                "dropoff_location": "Charlotte Douglas Airport",
                "distance_km": 15.5,
                "customer_id": "CUST_0042",
                "base_price": 38.75,
                "surge_multiplier": 1.5,
                "final_price": 58.13,
                "reasoning": "High demand during evening rush hour with rainy weather conditions. Customer is Gold tier with excellent history.",
                "confidence_score": 0.92,
                "created_at": "2024-12-01T18:30:00"
            }
        }


class RideHistoryItem(BaseModel):
    """Model for ride history items"""
    ride_id: str
    pickup_location: str
    dropoff_location: str
    distance_km: float
    final_price: float
    created_at: datetime


class PricingDecision(BaseModel):
    """
    Model for pricing decisions (pricing_decisions collection)
    
    Stores AI-generated pricing decisions separately from historical rides.
    """
    ride_id: str = Field(..., description="Reference to ride or unique ID")
    calculated_price: float = Field(..., description="Final calculated price")
    base_price: float = Field(..., description="Base price before surge")
    surge_multiplier: float = Field(..., description="Surge multiplier applied")
    reasoning: Optional[Dict[str, Any]] = Field(None, description="AI reasoning object")
    agent_trace: Optional[list] = Field(None, description="Agent execution trace")
    timestamp: datetime = Field(default_factory=datetime.now)
    applied: bool = Field(default=False, description="Whether pricing was applied")
    
    # Additional context
    customer_id: Optional[str] = Field(None, description="Customer ID")
    pickup_location: Optional[str] = Field(None, description="Pickup location")
    dropoff_location: Optional[str] = Field(None, description="Dropoff location")
    distance_km: Optional[float] = Field(None, description="Distance in km")
    time_of_day: Optional[str] = Field(None, description="Time of day")
    weather_condition: Optional[str] = Field(None, description="Weather condition")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ride_id": "a48e84c6f3c940beaa4f5567",
                "calculated_price": 324.49,
                "base_price": 221.35,
                "surge_multiplier": 1.47,
                "reasoning": {"factors": ["high_demand", "weather"]},
                "agent_trace": [],
                "timestamp": "2025-11-25T06:50:09",
                "applied": False,
                "customer_id": "CUST-478712",
                "confidence_score": 0.92
            }
        }

