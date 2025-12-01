"""
Weather Data Tool - Fetches weather conditions affecting pricing
"""
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import json
from datetime import datetime


class WeatherDataInput(BaseModel):
    """Input schema for weather queries"""
    city: str = Field(description="City to get weather for")
    scheduled_time: Optional[str] = Field(default=None, description="ISO timestamp for scheduled rides")


class WeatherDataTool(BaseTool):
    """Tool for fetching weather data that affects pricing"""
    
    name: str = "weather_data"
    description: str = """
    Get current or forecasted weather conditions for a city.
    Weather affects pricing: storms increase prices for driver safety.
    Use scheduled_time for future rides to get forecast.
    """
    args_schema: Type[BaseModel] = WeatherDataInput
    
    def _run(
        self,
        city: str,
        scheduled_time: Optional[str] = None
    ) -> str:
        """Fetch weather data (mock implementation for now)"""
        
        # TODO: Replace with actual weather API when ready
        # import requests
        # response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}")
        
        # Mock weather responses for development
        import random
        
        weather_conditions = [
            {"condition": "clear", "severity": "none", "temp": 72, "multiplier": 1.0},
            {"condition": "light_rain", "severity": "light", "temp": 65, "multiplier": 1.1},
            {"condition": "heavy_rain", "severity": "moderate", "temp": 58, "multiplier": 1.25},
            {"condition": "thunderstorm", "severity": "severe", "temp": 55, "multiplier": 1.5},
            {"condition": "snow", "severity": "moderate", "temp": 28, "multiplier": 1.4},
            {"condition": "fog", "severity": "moderate", "temp": 50, "multiplier": 1.2},
        ]
        
        # For scheduled rides, use different weather (simulating forecast)
        if scheduled_time:
            weather = random.choice(weather_conditions)
            forecast_type = "forecast"
        else:
            # Current weather - bias towards clear
            weather = weather_conditions[0] if random.random() < 0.7 else random.choice(weather_conditions[1:])
            forecast_type = "current"
        
        return json.dumps({
            "city": city,
            "type": forecast_type,
            "condition": weather["condition"],
            "severity": weather["severity"],
            "temperature": weather["temp"],
            "pricing_multiplier": weather["multiplier"],
            "recommendation": f"Apply {weather['multiplier']}x multiplier for {weather['condition']} conditions",
            "timestamp": scheduled_time or datetime.now().isoformat()
        })
    
    async def _arun(self, *args, **kwargs):
        """Async version"""
        return self._run(*args, **kwargs)

