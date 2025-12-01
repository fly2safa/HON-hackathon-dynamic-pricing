"""
Pricing Data Models

Pydantic models for pricing calculation requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PricingRequest(BaseModel):
    """
    Request model for pricing calculations
    
    This model is used when the frontend requests a price quote
    without creating a full ride record.
    """
    pickup_location: str = Field(..., description="Starting location")
    dropoff_location: str = Field(..., description="Destination location")
    distance_km: float = Field(..., gt=0, description="Distance in kilometers")
    customer_id: str = Field(..., description="Customer identifier")
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
                "weather_condition": "clear"
            }
        }


class PricingResponse(BaseModel):
    """
    Response model for pricing calculations
    
    Contains the calculated price and AI reasoning.
    """
    base_price: float = Field(..., description="Base price before surge")
    surge_multiplier: float = Field(..., ge=1.0, description="Surge pricing multiplier")
    final_price: float = Field(..., description="Final calculated price")
    reasoning: str = Field(..., description="AI agent's pricing reasoning")
    confidence_score: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Agent's confidence in the pricing decision (0-1)"
    )
    agent_trace_url: Optional[str] = Field(
        None,
        description="LangSmith trace URL for observability"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the pricing calculation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "base_price": 38.75,
                "surge_multiplier": 1.5,
                "final_price": 58.13,
                "reasoning": "High demand during evening rush hour. Weather conditions are clear. Customer has Gold tier status.",
                "confidence_score": 0.92,
                "agent_trace_url": "https://smith.langchain.com/public/trace-id-here",
                "metadata": {
                    "customer_tier": "Gold",
                    "historical_avg_price": 42.50,
                    "current_demand": "high"
                }
            }
        }


class PricingFactors(BaseModel):
    """
    Model for pricing factors used in calculations
    
    Internal model used by the pricing agent.
    """
    base_rate_per_km: float = Field(default=2.5, description="Base rate per kilometer")
    time_multiplier: float = Field(default=1.0, description="Time-based multiplier")
    weather_multiplier: float = Field(default=1.0, description="Weather-based multiplier")
    demand_multiplier: float = Field(default=1.0, description="Demand-based multiplier")
    customer_tier_discount: float = Field(default=0.0, description="Loyalty discount")

