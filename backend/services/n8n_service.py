"""
n8n Workflow Service

Integrates with n8n webhooks for external data enrichment.

Owner: Steve (Role 6)
Created: Dec 2, 2025
"""

import httpx
import logging
from typing import Optional, Dict, Any
import os
import json

logger = logging.getLogger(__name__)

# n8n webhook URLs (configurable via environment)
N8N_BASE_URL = os.getenv("N8N_BASE_URL", "http://localhost:5678")
N8N_WEATHER_WEBHOOK = os.getenv("N8N_WEATHER_WEBHOOK", f"{N8N_BASE_URL}/webhook/weather-data")
N8N_EVENTS_WEBHOOK = os.getenv("N8N_EVENTS_WEBHOOK", f"{N8N_BASE_URL}/webhook/event-data")
N8N_TRAFFIC_WEBHOOK = os.getenv("N8N_TRAFFIC_WEBHOOK", f"{N8N_BASE_URL}/webhook/traffic-data")
N8N_PRICING_WEBHOOK = os.getenv("N8N_PRICING_WEBHOOK", f"{N8N_BASE_URL}/webhook/pricing-enrichment")

# Timeout for n8n requests (seconds)
N8N_TIMEOUT = float(os.getenv("N8N_TIMEOUT", "10"))


class N8nService:
    """
    Service for calling n8n workflow webhooks.
    
    Provides external data enrichment for:
    - Weather conditions
    - Local events
    - Traffic data
    - Combined pricing factors
    """
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=N8N_TIMEOUT)
        self._n8n_available = None
        logger.info("N8nService initialized")
    
    async def check_availability(self) -> bool:
        """Check if n8n is running and accessible."""
        try:
            # Simple health check - try to reach n8n
            response = await self.client.get(f"{N8N_BASE_URL}/healthz", timeout=2)
            self._n8n_available = response.status_code == 200
        except Exception:
            self._n8n_available = False
        return self._n8n_available
    
    async def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data for pricing adjustment.
        
        Args:
            city: City name (e.g., "Phoenix", "New York")
            
        Returns:
            Weather data with pricing multiplier, or None if unavailable
        """
        try:
            response = await self.client.post(
                N8N_WEATHER_WEBHOOK,
                json={"city": city}
            )
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Weather data for {city}: {data.get('conditions')}, multiplier: {data.get('pricing_multiplier')}")
                return data
            else:
                logger.warning(f"Weather webhook returned {response.status_code}")
                return None
        except httpx.TimeoutException:
            logger.warning(f"Weather webhook timeout for {city}")
            return None
        except Exception as e:
            logger.error(f"Weather webhook error: {e}")
            return None
    
    async def get_events_data(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Fetch nearby events that may affect pricing.
        
        Args:
            city: City name
            
        Returns:
            Events data with pricing multiplier, or None if unavailable
        """
        try:
            response = await self.client.post(
                N8N_EVENTS_WEBHOOK,
                json={"city": city}
            )
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Events for {city}: {data.get('event_count')} events, multiplier: {data.get('pricing_multiplier')}")
                return data
            else:
                logger.warning(f"Events webhook returned {response.status_code}")
                return None
        except httpx.TimeoutException:
            logger.warning(f"Events webhook timeout for {city}")
            return None
        except Exception as e:
            logger.error(f"Events webhook error: {e}")
            return None
    
    async def get_traffic_data(
        self, 
        city: str, 
        origin: str, 
        destination: str,
        distance_miles: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch traffic conditions for route.
        
        Args:
            city: City name
            origin: Starting point
            destination: End point
            distance_miles: Optional distance estimate
            
        Returns:
            Traffic data with pricing multiplier, or None if unavailable
        """
        try:
            response = await self.client.post(
                N8N_TRAFFIC_WEBHOOK,
                json={
                    "city": city,
                    "origin": origin,
                    "destination": destination,
                    "distance_miles": distance_miles or 15
                }
            )
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Traffic for {city}: {data.get('traffic_level')}, multiplier: {data.get('pricing_multiplier')}")
                return data
            else:
                logger.warning(f"Traffic webhook returned {response.status_code}")
                return None
        except httpx.TimeoutException:
            logger.warning(f"Traffic webhook timeout for {city}")
            return None
        except Exception as e:
            logger.error(f"Traffic webhook error: {e}")
            return None
    
    async def get_pricing_enrichment(
        self,
        city: str,
        origin: str,
        destination: str,
        distance_miles: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get combined pricing enrichment from all external factors.
        
        This calls the master workflow that aggregates:
        - Weather conditions
        - Traffic data
        - Event detection
        
        Args:
            city: City name
            origin: Starting point
            destination: End point
            distance_miles: Optional distance estimate
            
        Returns:
            Combined pricing data with final multiplier and reasoning
        """
        try:
            response = await self.client.post(
                N8N_PRICING_WEBHOOK,
                json={
                    "city": city,
                    "origin": origin,
                    "destination": destination,
                    "distance_miles": distance_miles or 15
                }
            )
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Pricing enrichment for {city}: multiplier {data.get('pricing', {}).get('final_multiplier')}")
                return data
            else:
                logger.warning(f"Pricing webhook returned {response.status_code}")
                return None
        except httpx.TimeoutException:
            logger.warning(f"Pricing webhook timeout for {city}")
            return None
        except Exception as e:
            logger.error(f"Pricing webhook error: {e}")
            return None
    
    async def get_all_enrichment_data(
        self,
        city: str,
        origin: str = "Downtown",
        destination: str = "Airport",
        distance_miles: float = 15
    ) -> Dict[str, Any]:
        """
        Fetch all enrichment data with fallback to mock data.
        
        Returns combined data even if some sources fail.
        """
        result = {
            "city": city,
            "origin": origin,
            "destination": destination,
            "weather": None,
            "events": None,
            "traffic": None,
            "combined_multiplier": 1.0,
            "reasoning": [],
            "data_sources": {
                "weather": "unavailable",
                "events": "unavailable", 
                "traffic": "unavailable"
            }
        }
        
        # Try to get weather
        weather = await self.get_weather_data(city)
        if weather:
            result["weather"] = weather
            result["data_sources"]["weather"] = "live"
            if weather.get("pricing_multiplier", 1.0) > 1.0:
                result["reasoning"].append(weather.get("reasoning", "Weather impact"))
        
        # Try to get events
        events = await self.get_events_data(city)
        if events:
            result["events"] = events
            result["data_sources"]["events"] = "live"
            if events.get("pricing_multiplier", 1.0) > 1.0:
                result["reasoning"].append(events.get("reasoning", "Event impact"))
        
        # Try to get traffic
        traffic = await self.get_traffic_data(city, origin, destination, distance_miles)
        if traffic:
            result["traffic"] = traffic
            result["data_sources"]["traffic"] = "live"
            if traffic.get("pricing_multiplier", 1.0) > 1.0:
                result["reasoning"].append(traffic.get("reasoning", "Traffic impact"))
        
        # Calculate combined multiplier
        multipliers = [
            result["weather"].get("pricing_multiplier", 1.0) if result["weather"] else 1.0,
            result["events"].get("pricing_multiplier", 1.0) if result["events"] else 1.0,
            result["traffic"].get("pricing_multiplier", 1.0) if result["traffic"] else 1.0
        ]
        
        # Combine multipliers (capped at 2.5x to prevent extreme prices)
        combined = 1 + sum((m - 1) for m in multipliers) * 0.7
        result["combined_multiplier"] = min(round(combined, 2), 2.5)
        
        if not result["reasoning"]:
            result["reasoning"] = ["Standard pricing conditions"]
        
        return result
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global instance
n8n_service: Optional[N8nService] = None


def get_n8n_service() -> N8nService:
    """Dependency injection for FastAPI."""
    global n8n_service
    if n8n_service is None:
        n8n_service = N8nService()
    return n8n_service


async def init_n8n_service():
    """Initialize the n8n service on startup."""
    global n8n_service
    n8n_service = N8nService()
    available = await n8n_service.check_availability()
    if available:
        logger.info("✅ n8n service connected")
    else:
        logger.warning("⚠️ n8n not available - external enrichment will be skipped")
    return n8n_service
