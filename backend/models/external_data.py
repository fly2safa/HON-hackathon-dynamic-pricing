"""
External Data Models

Pydantic models for external data (weather, traffic, events) validation and serialization.
Matches existing MongoDB schema.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
from datetime import datetime


class ExternalDataBase(BaseModel):
    """Base external data model"""
    data_type: str = Field(..., description="Type of data: weather, traffic, events")
    location: str = Field(..., description="Location/zone for the data")
    data: Dict[str, Any] = Field(..., description="The actual external data")


class ExternalData(ExternalDataBase):
    """
    Full external data model
    
    Matches existing MongoDB external_data collection schema.
    Stores enrichment data from external APIs (weather, traffic, events).
    """
    timestamp: datetime = Field(default_factory=datetime.now, description="When data was fetched")
    ttl: Optional[datetime] = Field(None, description="Time to live - when data expires")
    
    class Config:
        json_schema_extra = {
            "example": {
                "data_type": "weather",
                "location": "Urban",
                "timestamp": "2025-11-27T17:29:57",
                "data": {
                    "temperature": 72,
                    "condition": "Clear",
                    "humidity": 65,
                    "wind_speed": 10
                },
                "ttl": "2025-11-27T23:23:57"
            }
        }
        from_attributes = True


class WeatherData(BaseModel):
    """Model for weather data specifically"""
    temperature: Optional[float] = Field(None, description="Temperature in Fahrenheit")
    condition: Optional[str] = Field(None, description="Weather condition (Clear, Rainy, etc.)")
    humidity: Optional[float] = Field(None, description="Humidity percentage")
    wind_speed: Optional[float] = Field(None, description="Wind speed in mph")
    precipitation: Optional[float] = Field(None, description="Precipitation amount")


class TrafficData(BaseModel):
    """Model for traffic data specifically"""
    congestion_level: Optional[str] = Field(None, description="Traffic congestion: Low, Medium, High")
    average_speed: Optional[float] = Field(None, description="Average speed in mph")
    incidents: Optional[int] = Field(None, description="Number of traffic incidents")
    estimated_delay: Optional[int] = Field(None, description="Estimated delay in minutes")


class EventData(BaseModel):
    """Model for event data specifically"""
    event_name: Optional[str] = Field(None, description="Name of the event")
    event_type: Optional[str] = Field(None, description="Type: concert, sports, conference, etc.")
    venue: Optional[str] = Field(None, description="Venue name")
    start_time: Optional[datetime] = Field(None, description="Event start time")
    expected_attendance: Optional[int] = Field(None, description="Expected number of attendees")


class ExternalDataCreate(ExternalDataBase):
    """Model for creating external data records"""
    ttl: Optional[datetime] = Field(None, description="Time to live - when data should expire")


class ExternalDataQuery(BaseModel):
    """Model for querying external data"""
    data_type: Optional[Literal["weather", "traffic", "events"]] = Field(
        None,
        description="Filter by data type"
    )
    location: Optional[str] = Field(None, description="Filter by location")
    min_timestamp: Optional[datetime] = Field(None, description="Filter by minimum timestamp")
    max_timestamp: Optional[datetime] = Field(None, description="Filter by maximum timestamp")


class ExternalDataSummary(BaseModel):
    """Model for external data summary"""
    data_type: str
    location: str
    latest_timestamp: datetime
    record_count: int

