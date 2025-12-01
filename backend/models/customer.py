"""
Customer Data Models

Pydantic models for customer-related data validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    """Base customer model with common fields"""
    customer_id: str = Field(..., description="Unique customer identifier")
    name: Optional[str] = Field(None, description="Customer name")


class Customer(CustomerBase):
    """
    Full customer model with all fields
    
    Used for MongoDB storage and retrieval.
    """
    loyalty_status: str = Field(
        default="Silver",
        description="Loyalty tier: Bronze, Silver, Gold, Platinum"
    )
    total_rides: int = Field(default=0, ge=0, description="Total number of rides")
    total_spent: float = Field(default=0.0, ge=0, description="Total amount spent")
    average_rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Average customer rating (0-5)"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_0042",
                "name": "John Doe",
                "loyalty_status": "Gold",
                "total_rides": 127,
                "total_spent": 3847.50,
                "average_rating": 4.8,
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-12-01T18:30:00"
            }
        }


class CustomerCreate(CustomerBase):
    """Model for creating new customers"""
    name: str = Field(..., description="Customer name")
    loyalty_status: str = Field(default="Bronze", description="Initial loyalty tier")


class CustomerUpdate(BaseModel):
    """Model for updating customer information"""
    name: Optional[str] = None
    loyalty_status: Optional[str] = None
    average_rating: Optional[float] = Field(None, ge=0, le=5)


class CustomerStats(BaseModel):
    """Model for customer statistics"""
    customer_id: str
    total_rides: int
    total_spent: float
    average_price_per_ride: float
    loyalty_status: str
    favorite_routes: list[str] = Field(default_factory=list)

