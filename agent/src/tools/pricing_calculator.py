"""
Pricing Calculator Tool - Calculates base pricing with various factors
"""
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field


class PricingCalculatorInput(BaseModel):
    """Input schema for pricing calculator"""
    distance: float = Field(description="Distance in miles")
    duration: int = Field(description="Estimated duration in minutes")
    passenger_count: int = Field(description="Number of passengers")
    city: str = Field(description="City/market for the ride")
    surge_multiplier: float = Field(default=1.0, description="Surge pricing multiplier")
    loyalty_discount: float = Field(default=0.0, description="Loyalty discount (0-0.20)")


class PricingCalculatorTool(BaseTool):
    """Tool for calculating ride pricing with multiple factors"""
    
    name: str = "pricing_calculator"
    description: str = """
    Calculates ride pricing based on distance, duration, passengers, city, surge, and loyalty.
    Use this to compute base price and apply multipliers.
    Returns: base_price, dynamic_price, driver_earnings
    """
    args_schema: Type[BaseModel] = PricingCalculatorInput
    
    def _run(
        self,
        distance: float,
        duration: int,
        passenger_count: int,
        city: str,
        surge_multiplier: float = 1.0,
        loyalty_discount: float = 0.0
    ) -> dict:
        """Calculate pricing"""
        
        # City-based pricing multipliers
        city_multipliers = {
            'Phoenix': 1.0,
            'New York': 1.4,
            'San Francisco': 1.5,
            'Chicago': 1.2,
            'Tampa': 0.95,
        }
        
        city_multiplier = city_multipliers.get(city, 1.0)
        
        # Base price calculation
        base_price = (5.0 + (distance * 2.5) + (passenger_count * 1.5)) * city_multiplier
        
        # Apply surge
        price_before_discount = base_price * surge_multiplier
        
        # Apply loyalty discount
        dynamic_price = price_before_discount * (1 - loyalty_discount)
        
        # Driver earnings (80% of final price)
        driver_earnings = dynamic_price * 0.8
        
        return {
            "base_price": round(base_price, 2),
            "price_before_discount": round(price_before_discount, 2),
            "dynamic_price": round(dynamic_price, 2),
            "driver_earnings": round(driver_earnings, 2),
            "city_multiplier": city_multiplier,
            "surge_multiplier": surge_multiplier,
            "loyalty_discount": loyalty_discount,
            "discount_amount": round(price_before_discount - dynamic_price, 2)
        }
    
    async def _arun(self, *args, **kwargs):
        """Async version"""
        return self._run(*args, **kwargs)

