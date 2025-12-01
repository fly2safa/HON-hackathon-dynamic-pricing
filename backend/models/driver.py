"""
Driver Data Models

Pydantic models for driver-related data validation and serialization.
Matches existing MongoDB schema.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DriverBase(BaseModel):
    """Base driver model with common fields"""
    driver_id: str = Field(..., description="Unique driver identifier")
    name: str = Field(..., description="Driver name")


class Driver(DriverBase):
    """
    Full driver model with all fields
    
    Matches existing MongoDB drivers collection schema.
    """
    status: str = Field(default="Active", description="Driver status: Active, Inactive, etc.")
    vehicle_type: str = Field(..., description="Type of vehicle: Economy, Premium, SUV, etc.")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Driver rating (0-5)")
    total_rides_completed: int = Field(default=0, ge=0, description="Total rides completed")
    total_earnings: float = Field(default=0.0, ge=0, description="Total earnings")
    current_location: Optional[str] = Field(None, description="Current location/zone")
    availability: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Driver availability details"
    )
    earnings_stats: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Earnings statistics and breakdowns"
    )
    incentives: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Incentive programs and bonuses"
    )
    performance_metrics: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Performance metrics and KPIs"
    )
    joined_date: Optional[datetime] = Field(None, description="Date driver joined")
    last_ride_date: Optional[datetime] = Field(None, description="Date of last completed ride")
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": "DRV-720620",
                "name": "Omar Jackson",
                "status": "Active",
                "vehicle_type": "Economy",
                "rating": 4.21,
                "total_rides_completed": 737,
                "total_earnings": 180344.35,
                "current_location": "Urban",
                "availability": {},
                "earnings_stats": {},
                "incentives": {},
                "performance_metrics": {},
                "joined_date": "2025-09-10T19:12:11",
                "last_ride_date": "2025-11-25T12:12:11"
            }
        }
        from_attributes = True


class DriverCreate(DriverBase):
    """Model for creating new drivers"""
    vehicle_type: str = Field(..., description="Type of vehicle")
    status: str = Field(default="Active", description="Initial status")


class DriverUpdate(BaseModel):
    """Model for updating driver information"""
    name: Optional[str] = None
    status: Optional[str] = None
    vehicle_type: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    current_location: Optional[str] = None
    availability: Optional[Dict[str, Any]] = None


class DriverStats(BaseModel):
    """Model for driver statistics"""
    driver_id: str
    name: str
    total_rides_completed: int
    total_earnings: float
    rating: float
    status: str
    vehicle_type: str
    average_earnings_per_ride: float

