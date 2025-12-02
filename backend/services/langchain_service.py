"""
AI Pricing Service - OpenAI Integration

Uses OpenAI directly to generate intelligent pricing explanations.
Bypasses LangChain dependency issues for simpler, more reliable integration.

Author: Safa (Role 4 - LangChain/Agent Engineer)
Created: Dec 2, 2025
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from root .env
load_dotenv(dotenv_path='../.env')

logger = logging.getLogger(__name__)

# Try to import OpenAI directly - much simpler than LangChain
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
    logger.info("✅ OpenAI imports successful")
except ImportError as e:
    OPENAI_AVAILABLE = False
    logger.warning(f"OpenAI not available - using mock reasoning. Error: {e}")


class LangChainPricingService:
    """
    Service for generating AI-powered pricing reasoning using OpenAI directly.
    """
    
    def __init__(self):
        self.client = None
        self.is_initialized = False
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI not installed - AI reasoning disabled")
            return
        
        # Try OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and (openai_key.startswith('sk-') or openai_key.startswith('sk-proj-')):
            try:
                self.client = AsyncOpenAI(api_key=openai_key)
                self.is_initialized = True
                logger.info("✅ OpenAI client initialized successfully")
                return
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI: {e}")
        
        logger.warning("⚠️ No valid OpenAI API key found - AI reasoning will use fallback")
    
    async def generate_pricing_reasoning(
        self,
        pickup: str,
        dropoff: str,
        distance_km: float,
        base_price: float,
        final_price: float,
        surge_multiplier: float,
        time_of_day: str,
        weather_condition: Optional[str] = None,
        customer_id: Optional[str] = None,
        city: Optional[str] = None,
        city_multiplier: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate AI-powered reasoning for a pricing decision.
        
        Returns:
            Dict with 'reasoning' (str) and 'ai_generated' (bool)
        """
        if not self.is_initialized or not self.client:
            return self._generate_fallback_reasoning(
                distance_km, base_price, final_price, 
                surge_multiplier, time_of_day, weather_condition
            )
        
        try:
            # Create the prompt
            system_prompt = """You are HoneyGo's AI pricing analyst. Generate a brief, professional explanation 
for a ride pricing decision. Be concise (3-4 sentences max). Include specific factors that influenced the price.
Format: Start each reason on a new line. Be specific about numbers and conditions.
Consider city-specific factors like regulations, cost of living, and market demand."""

            # Add city context
            city_context = ""
            if city and city != "Unknown":
                city_notes = {
                    "New York": "NYC has congestion pricing, high demand, and strict regulations",
                    "San Francisco": "Tech hub with high cost of living and strong demand",
                    "Chicago": "Midwest hub with moderate regulations and seasonal demand",
                    "Phoenix": "Lower cost of living, base pricing market",
                    "Orlando": "Tourism-driven market with variable demand",
                }
                city_context = f"\nCity: {city} ({city_notes.get(city, 'Standard market')})"
                city_context += f"\nCity Multiplier: {city_multiplier:.2f}x"

            user_prompt = f"""Explain this ride pricing decision:

Route: {pickup} → {dropoff}
Distance: {distance_km:.1f} km
Time: {time_of_day}
Weather: {weather_condition or 'Clear'}{city_context}
Base Price: ${base_price:.2f}
Surge Multiplier: {surge_multiplier:.2f}x
Final Price: ${final_price:.2f}

Provide 3-4 brief reasons for this pricing, including city-specific factors if applicable."""

            # Call OpenAI directly
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            reasoning = response.choices[0].message.content.strip()
            
            logger.info(f"✅ AI reasoning generated for {pickup} → {dropoff}")
            
            return {
                'reasoning': reasoning,
                'ai_generated': True,
                'model': 'gpt-3.5-turbo'
            }
            
        except Exception as e:
            logger.error(f"❌ AI reasoning failed: {e}")
            return self._generate_fallback_reasoning(
                distance_km, base_price, final_price,
                surge_multiplier, time_of_day, weather_condition
            )
    
    def _generate_fallback_reasoning(
        self,
        distance_km: float,
        base_price: float,
        final_price: float,
        surge_multiplier: float,
        time_of_day: str,
        weather_condition: Optional[str]
    ) -> Dict[str, Any]:
        """Generate rule-based reasoning when AI is not available."""
        
        reasons = [f"Base rate: ${base_price:.2f} ({distance_km:.1f}km × $2.50/km)"]
        
        if surge_multiplier > 1.0:
            time_labels = {
                'morning': 'morning rush hour',
                'evening': 'evening rush hour', 
                'night': 'late night hours',
                'afternoon': 'afternoon hours'
            }
            time_label = time_labels.get(time_of_day, time_of_day)
            reasons.append(f"Time surge: {time_label} (×{surge_multiplier:.1f})")
            
            if weather_condition and weather_condition.lower() not in ['clear', 'cloudy']:
                reasons.append(f"Weather impact: {weather_condition} conditions increase demand")
        else:
            reasons.append("Standard pricing - normal demand period")
        
        reasons.append(f"Final price: ${final_price:.2f}")
        
        return {
            'reasoning': '. '.join(reasons),
            'ai_generated': False,
            'model': 'rule-based'
        }


# Singleton instance
_langchain_service: Optional[LangChainPricingService] = None


def get_langchain_service() -> LangChainPricingService:
    """Get or create the LangChain service singleton."""
    global _langchain_service
    if _langchain_service is None:
        _langchain_service = LangChainPricingService()
    return _langchain_service

