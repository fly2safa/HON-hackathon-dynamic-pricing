"""
n8n Workflow Integration Router

API endpoints for n8n workflow webhooks (weather, events, traffic).

Owner: Steve (Role 6)
Created: Dec 2, 2025
"""

from fastapi import APIRouter, Query, Body
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime, timedelta
from collections import deque

from services.n8n_service import get_n8n_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/n8n", tags=["n8n-workflows"])

# In-memory notification store (for demo/presentation purposes)
# In production, use Redis or a database
_notification_store: deque = deque(maxlen=50)  # Keep last 50 notifications


@router.get("/health")
async def check_n8n_health():
    """Check if n8n workflows are available."""
    service = get_n8n_service()
    available = await service.check_availability()
    return {
        "n8n_available": available,
        "message": "n8n connected" if available else "n8n not running - using fallback data"
    }


@router.get("/weather/{city}")
async def get_weather(city: str):
    """
    Get weather data for a city via n8n workflow.
    
    Returns weather conditions and pricing multiplier.
    """
    service = get_n8n_service()
    data = await service.get_weather_data(city)
    
    if data:
        return {"source": "n8n_live", "data": data}
    else:
        return {
            "source": "mock_fallback",
            "data": {
                "city": city,
                "conditions": "Clear",
                "temperature_f": 75,
                "pricing_multiplier": 1.0,
                "reasoning": "Weather data unavailable - using default"
            }
        }


@router.get("/events/{city}")
async def get_events(city: str):
    """
    Get nearby events for a city via n8n workflow.
    
    Returns events and pricing multiplier for surge areas.
    """
    service = get_n8n_service()
    data = await service.get_events_data(city)
    
    if data:
        return {"source": "n8n_live", "data": data}
    else:
        return {
            "source": "mock_fallback",
            "data": {
                "city": city,
                "events": [],
                "event_count": 0,
                "pricing_multiplier": 1.0,
                "reasoning": "No event data available"
            }
        }


@router.get("/traffic")
async def get_traffic(
    city: str = Query(..., description="City name"),
    origin: str = Query("Downtown", description="Starting location"),
    destination: str = Query("Airport", description="Destination"),
    distance_miles: Optional[float] = Query(15, description="Estimated distance")
):
    """
    Get traffic conditions for a route via n8n workflow.
    
    Returns traffic level and pricing multiplier.
    """
    service = get_n8n_service()
    data = await service.get_traffic_data(city, origin, destination, distance_miles)
    
    if data:
        return {"source": "n8n_live", "data": data}
    else:
        return {
            "source": "mock_fallback",
            "data": {
                "city": city,
                "origin": origin,
                "destination": destination,
                "traffic_level": "moderate",
                "pricing_multiplier": 1.1,
                "reasoning": "Traffic data unavailable - using estimate"
            }
        }


@router.post("/enrichment")
async def get_pricing_enrichment(
    city: str = Query(..., description="City name"),
    origin: str = Query("Downtown", description="Starting location"),
    destination: str = Query("Airport", description="Destination"),
    distance_miles: Optional[float] = Query(15, description="Estimated distance")
):
    """
    Get combined pricing enrichment from all n8n workflows.
    
    Aggregates weather, events, and traffic data into a single
    pricing multiplier with detailed reasoning.
    
    This is the main endpoint the agent should call.
    """
    service = get_n8n_service()
    data = await service.get_all_enrichment_data(
        city=city,
        origin=origin,
        destination=destination,
        distance_miles=distance_miles
    )
    
    return {"success": True, "data": data}


@router.get("/demo/compare-cities")
async def compare_cities(
    city1: str = Query("Phoenix", description="First city"),
    city2: str = Query("New York", description="Second city")
):
    """
    Compare external factors between two cities.
    
    Useful for demo to show how different conditions
    affect pricing in different locations.
    
    This supports Steve's two-city comparison demo idea!
    """
    service = get_n8n_service()
    
    data1 = await service.get_all_enrichment_data(city1)
    data2 = await service.get_all_enrichment_data(city2)
    
    return {
        "comparison": {
            city1: {
                "multiplier": data1["combined_multiplier"],
                "weather": data1.get("weather", {}).get("conditions", "Unknown"),
                "traffic": data1.get("traffic", {}).get("traffic_level", "Unknown"),
                "reasoning": data1["reasoning"]
            },
            city2: {
                "multiplier": data2["combined_multiplier"],
                "weather": data2.get("weather", {}).get("conditions", "Unknown"),
                "traffic": data2.get("traffic", {}).get("traffic_level", "Unknown"),
                "reasoning": data2["reasoning"]
            }
        },
        "price_difference_percent": round(
            (data2["combined_multiplier"] - data1["combined_multiplier"]) / data1["combined_multiplier"] * 100, 
            1
        )
    }


@router.post("/notifications")
async def create_notification(
    notification: Dict[str, Any] = Body(..., description="Notification data")
):
    """
    Create a notification from n8n workflow.
    
    This endpoint is called by n8n workflows to trigger pop-out notifications
    in the frontend during presentations.
    
    Expected format:
    {
        "title": "Pricing Update",
        "message": "Surge pricing activated in Phoenix",
        "type": "info",  # success, info, warning, error
        "duration": 5000,  # milliseconds (optional)
        "action": {  # optional
            "label": "View Details",
            "url": "http://localhost:3000/surge-pricing"
        }
    }
    """
    notification_data = {
        "id": f"n8n-{datetime.now().timestamp()}-{len(_notification_store)}",
        "title": notification.get("title", "n8n Notification"),
        "message": notification.get("message", ""),
        "type": notification.get("type", "info"),
        "duration": notification.get("duration", 5000),
        "timestamp": datetime.now().isoformat(),
    }
    
    if "action" in notification:
        notification_data["action"] = notification["action"]
    
    _notification_store.append(notification_data)
    logger.info(f"Notification created: {notification_data['title']}")
    
    return {"success": True, "notification_id": notification_data["id"]}


@router.get("/notifications")
async def get_notifications(
    since: Optional[str] = Query(None, description="ISO timestamp to get notifications since")
):
    """
    Get pending notifications for the frontend.
    
    Frontend polls this endpoint to display pop-out notifications.
    Notifications are returned once and then removed from the queue.
    """
    now = datetime.now()
    cutoff_time = None
    
    if since:
        try:
            cutoff_time = datetime.fromisoformat(since.replace('Z', '+00:00'))
        except:
            pass
    
    # Get notifications that haven't expired (older than 1 minute are considered stale)
    stale_cutoff = now - timedelta(minutes=1)
    fresh_notifications = []
    
    while _notification_store:
        notif = _notification_store.popleft()
        notif_time = datetime.fromisoformat(notif["timestamp"])
        
        # Skip stale notifications
        if notif_time < stale_cutoff:
            continue
        
        # If since parameter provided, only return newer notifications
        if cutoff_time and notif_time <= cutoff_time:
            _notification_store.appendleft(notif)  # Put it back
            break
        
        fresh_notifications.append(notif)
    
    return {
        "notifications": fresh_notifications,
        "count": len(fresh_notifications)
    }
