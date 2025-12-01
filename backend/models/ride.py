"""
Ride Data Models

Pydantic models for ride-related data validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RideBase(BaseModel):
    """Base ride model with common fields"""
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

