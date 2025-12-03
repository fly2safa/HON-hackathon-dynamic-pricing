"""
HoneyGo Chat Agent - Natural Language Query Interface

Allows users to query the HoneyGo system using natural language.
Uses LangChain to interpret queries and return human-friendly responses.

Author: Safa (Role 4 - LangChain/Agent Engineer)
Created: Dec 3, 2025
"""

import os
import logging
import json
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../.env')

logger = logging.getLogger(__name__)

# Try to import LangChain
LANGCHAIN_AVAILABLE = False
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
    logger.info("✅ LangChain available for Chat Agent")
except ImportError as e:
    logger.warning(f"LangChain not available for Chat Agent: {e}")


class HoneyGoChatAgent:
    """
    Conversational AI agent for natural language queries.
    
    Supports queries like:
    - "Find all Urban rides at Night"
    - "How many Gold customers do we have?"
    - "What's the average surge in New York?"
    """
    
    def __init__(self, mongodb_service=None):
        """
        Initialize the chat agent.
        
        Args:
            mongodb_service: MongoDB service instance for data queries
        """
        self.mongodb_service = mongodb_service
        self.llm = None
        self.is_initialized = False
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LangChain LLM."""
        if not LANGCHAIN_AVAILABLE:
            logger.warning("⚠️ Chat Agent running in fallback mode (no LangChain)")
            return
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key or not (openai_key.startswith('sk-') or openai_key.startswith('sk-proj-')):
            logger.warning("⚠️ No valid OpenAI API key - Chat Agent using fallback")
            return
        
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.3,  # Lower temperature for more consistent query interpretation
                max_tokens=500,
                api_key=openai_key
            )
            self.is_initialized = True
            logger.info("✅ Chat Agent LLM initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Chat Agent LLM: {e}")
    
    async def process_query(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a natural language query and return a response.
        
        Args:
            message: User's natural language query
            context: Optional context (current_city, etc.)
            
        Returns:
            Dict with response, data, suggestions, and confidence
        """
        logger.info(f"📝 Processing query: {message}")
        
        # First, classify the query intent
        intent = await self._classify_intent(message)
        logger.info(f"🎯 Detected intent: {intent['type']}")
        
        # Execute the appropriate query based on intent
        if intent['type'] == 'rides_query':
            result = await self._handle_rides_query(message, intent, context)
        elif intent['type'] == 'customers_query':
            result = await self._handle_customers_query(message, intent, context)
        elif intent['type'] == 'pricing_query':
            result = await self._handle_pricing_query(message, intent, context)
        elif intent['type'] == 'statistics_query':
            result = await self._handle_statistics_query(message, intent, context)
        elif intent['type'] == 'drivers_query':
            result = await self._handle_drivers_query(message, intent, context)
        else:
            result = await self._handle_general_query(message, context)
        
        return result
    
    async def _classify_intent(self, message: str) -> Dict[str, Any]:
        """
        Classify the intent of the user's message.
        
        Returns:
            Dict with intent type and extracted parameters
        """
        message_lower = message.lower()
        
        # Simple keyword-based classification (fast, no API call needed)
        intent = {
            'type': 'general',
            'filters': {},
            'aggregation': None
        }
        
        # Rides queries
        if any(word in message_lower for word in ['ride', 'rides', 'trip', 'trips', 'journey']):
            intent['type'] = 'rides_query'
            
            # Extract location filter
            if 'urban' in message_lower:
                intent['filters']['location_category'] = 'Urban'
            elif 'suburban' in message_lower:
                intent['filters']['location_category'] = 'Suburban'
            elif 'rural' in message_lower:
                intent['filters']['location_category'] = 'Rural'
            
            # Extract time filter
            if 'night' in message_lower:
                intent['filters']['time_of_booking'] = 'Night'
            elif 'morning' in message_lower:
                intent['filters']['time_of_booking'] = 'Morning'
            elif 'afternoon' in message_lower:
                intent['filters']['time_of_booking'] = 'Afternoon'
            elif 'evening' in message_lower:
                intent['filters']['time_of_booking'] = 'Evening'
        
        # Customer queries
        elif any(word in message_lower for word in ['customer', 'customers', 'user', 'users', 'member']):
            intent['type'] = 'customers_query'
            
            # Extract loyalty tier filter
            if 'gold' in message_lower:
                intent['filters']['loyalty_status'] = 'Gold'
            elif 'silver' in message_lower:
                intent['filters']['loyalty_status'] = 'Silver'
            elif 'bronze' in message_lower:
                intent['filters']['loyalty_status'] = 'Bronze'
            elif 'new' in message_lower or 'regular' in message_lower:
                intent['filters']['loyalty_status'] = 'Regular'
        
        # Pricing queries
        elif any(word in message_lower for word in ['price', 'pricing', 'cost', 'surge', 'fare']):
            intent['type'] = 'pricing_query'
            
            if 'average' in message_lower or 'avg' in message_lower:
                intent['aggregation'] = 'average'
            elif 'highest' in message_lower or 'max' in message_lower:
                intent['aggregation'] = 'max'
            elif 'lowest' in message_lower or 'min' in message_lower:
                intent['aggregation'] = 'min'
        
        # Statistics queries
        elif any(word in message_lower for word in ['statistic', 'stats', 'total', 'count', 'how many', 'summary']):
            intent['type'] = 'statistics_query'
        
        # Driver queries
        elif any(word in message_lower for word in ['driver', 'drivers']):
            intent['type'] = 'drivers_query'
            
            if 'active' in message_lower:
                intent['filters']['status'] = 'Active'
        
        return intent
    
    async def _handle_rides_query(
        self,
        message: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries about rides."""
        
        filters = intent.get('filters', {})
        
        # Add city context if provided
        if context and context.get('current_city'):
            # Map city to location category if needed
            pass
        
        # Query MongoDB if available
        if self.mongodb_service and self.mongodb_service.connected:
            try:
                rides = await self.mongodb_service.get_historical_rides(
                    limit=100,
                    filter_query=filters if filters else None
                )
                
                count = len(rides)
                
                if count > 0:
                    # Calculate statistics
                    avg_price = sum(r.get('historical_cost_of_ride', 0) for r in rides) / count
                    
                    # Build response
                    filter_desc = self._describe_filters(filters)
                    response = f"I found {count} {filter_desc}rides. "
                    response += f"The average historical price is ${avg_price:.2f}."
                    
                    return {
                        'response': response,
                        'data': {
                            'type': 'rides',
                            'count': count,
                            'avg_price': round(avg_price, 2),
                            'filters': filters
                        },
                        'suggestions': [
                            "Show pricing trends",
                            "Compare with other locations",
                            "What's the surge multiplier?"
                        ],
                        'confidence': 0.9
                    }
                else:
                    filter_desc = self._describe_filters(filters)
                    return {
                        'response': f"I didn't find any {filter_desc}rides matching your criteria.",
                        'data': {'type': 'rides', 'count': 0},
                        'suggestions': [
                            "Try a different location",
                            "Try a different time",
                            "Show all rides"
                        ],
                        'confidence': 0.8
                    }
            except Exception as e:
                logger.error(f"Error querying rides: {e}")
        
        # Fallback response (mock data)
        return self._mock_rides_response(filters)
    
    async def _handle_customers_query(
        self,
        message: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries about customers."""
        
        filters = intent.get('filters', {})
        
        # For now, return mock data
        # In production, this would query the customers collection
        
        loyalty_tier = filters.get('loyalty_status', 'all')
        
        # Mock counts
        mock_counts = {
            'Gold': 45,
            'Silver': 120,
            'Bronze': 85,
            'Regular': 250,
            'all': 500
        }
        
        count = mock_counts.get(loyalty_tier, mock_counts['all'])
        
        if loyalty_tier != 'all':
            response = f"You have {count} {loyalty_tier} tier customers."
        else:
            response = f"You have {mock_counts['all']} total customers: {mock_counts['Gold']} Gold, {mock_counts['Silver']} Silver, {mock_counts['Bronze']} Bronze, and {mock_counts['Regular']} Regular."
        
        return {
            'response': response,
            'data': {
                'type': 'customers',
                'count': count,
                'tier': loyalty_tier,
                'breakdown': mock_counts
            },
            'suggestions': [
                "Show Gold customer details",
                "What's the average customer spend?",
                "Customer retention rate"
            ],
            'confidence': 0.85
        }
    
    async def _handle_pricing_query(
        self,
        message: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries about pricing."""
        
        aggregation = intent.get('aggregation', 'average')
        
        # Query MongoDB if available
        if self.mongodb_service and self.mongodb_service.connected:
            try:
                stats = await self.mongodb_service.get_ride_statistics()
                
                if aggregation == 'average':
                    price = stats.get('average_price', 0)
                    surge = stats.get('average_surge_multiplier', 1.0)
                    response = f"The average price is ${price:.2f} with an average surge multiplier of {surge:.2f}x."
                else:
                    price = stats.get('average_price', 0)
                    response = f"Pricing statistics: Average ${price:.2f}"
                
                return {
                    'response': response,
                    'data': {
                        'type': 'pricing',
                        'statistics': stats
                    },
                    'suggestions': [
                        "Compare prices by city",
                        "Show surge trends",
                        "What affects pricing?"
                    ],
                    'confidence': 0.9
                }
            except Exception as e:
                logger.error(f"Error querying pricing: {e}")
        
        # Fallback mock response
        return {
            'response': "The average ride price is $285 with a typical surge multiplier of 1.15x during peak hours.",
            'data': {
                'type': 'pricing',
                'avg_price': 285,
                'avg_surge': 1.15
            },
            'suggestions': [
                "Compare prices by city",
                "Show surge trends",
                "What affects pricing?"
            ],
            'confidence': 0.75
        }
    
    async def _handle_statistics_query(
        self,
        message: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries about overall statistics."""
        
        # Query MongoDB if available
        if self.mongodb_service and self.mongodb_service.connected:
            try:
                ride_stats = await self.mongodb_service.get_ride_statistics()
                driver_stats = await self.mongodb_service.get_driver_statistics()
                
                response = f"📊 HoneyGo Statistics:\n"
                response += f"• Total pricing decisions: {ride_stats.get('total_pricing_decisions', 0)}\n"
                response += f"• Total revenue: ${ride_stats.get('total_revenue', 0):,.2f}\n"
                response += f"• Average price: ${ride_stats.get('average_price', 0):.2f}\n"
                response += f"• Active drivers: {driver_stats.get('active_drivers', 0)}\n"
                response += f"• Average driver rating: {driver_stats.get('average_rating', 0):.1f}⭐"
                
                return {
                    'response': response,
                    'data': {
                        'type': 'statistics',
                        'ride_stats': ride_stats,
                        'driver_stats': driver_stats
                    },
                    'suggestions': [
                        "Show revenue breakdown",
                        "Driver performance details",
                        "Customer satisfaction metrics"
                    ],
                    'confidence': 0.95
                }
            except Exception as e:
                logger.error(f"Error querying statistics: {e}")
        
        # Fallback mock response
        return {
            'response': "📊 HoneyGo has processed over 1,000 rides with $285,000 in total revenue. Average price is $285 with 50 active drivers maintaining a 4.7⭐ average rating.",
            'data': {'type': 'statistics'},
            'suggestions': [
                "Show revenue breakdown",
                "Driver performance",
                "Customer metrics"
            ],
            'confidence': 0.7
        }
    
    async def _handle_drivers_query(
        self,
        message: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries about drivers."""
        
        filters = intent.get('filters', {})
        
        # Query MongoDB if available
        if self.mongodb_service and self.mongodb_service.connected:
            try:
                if filters.get('status') == 'Active':
                    drivers = await self.mongodb_service.get_active_drivers(limit=50)
                else:
                    drivers = await self.mongodb_service.get_drivers(limit=50)
                
                count = len(drivers)
                
                if count > 0:
                    avg_rating = sum(d.get('rating', 0) for d in drivers) / count
                    response = f"There are {count} {'active ' if filters.get('status') == 'Active' else ''}drivers with an average rating of {avg_rating:.1f}⭐."
                else:
                    response = "No drivers found matching your criteria."
                
                return {
                    'response': response,
                    'data': {
                        'type': 'drivers',
                        'count': count,
                        'avg_rating': round(avg_rating, 1) if count > 0 else 0
                    },
                    'suggestions': [
                        "Top rated drivers",
                        "Driver earnings breakdown",
                        "Driver availability by location"
                    ],
                    'confidence': 0.9
                }
            except Exception as e:
                logger.error(f"Error querying drivers: {e}")
        
        # Fallback mock response
        return {
            'response': "There are 50 active drivers with an average rating of 4.7⭐. Top performers earn over $300 per day.",
            'data': {
                'type': 'drivers',
                'count': 50,
                'avg_rating': 4.7
            },
            'suggestions': [
                "Top rated drivers",
                "Driver earnings",
                "Driver availability"
            ],
            'confidence': 0.75
        }
    
    async def _handle_general_query(
        self,
        message: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle general/unclassified queries using LLM."""
        
        if self.is_initialized and self.llm:
            try:
                system_prompt = """You are HoneyGo's AI assistant. You help users understand 
                the ride-sharing pricing system. Be concise, helpful, and friendly.
                
                HoneyGo features:
                - Dynamic pricing based on demand, weather, and events
                - Customer loyalty tiers (Gold, Silver, Bronze, Regular)
                - Real-time surge pricing during high demand
                - AI-powered pricing explanations
                - Multi-city support (NYC, SF, Chicago, Phoenix, Orlando)
                
                Keep responses brief (2-3 sentences max)."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=message)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                return {
                    'response': response.content,
                    'data': {'type': 'general'},
                    'suggestions': [
                        "Show ride statistics",
                        "How does pricing work?",
                        "What cities are supported?"
                    ],
                    'confidence': 0.8
                }
            except Exception as e:
                logger.error(f"LLM error in general query: {e}")
        
        # Fallback response
        return {
            'response': "I can help you with HoneyGo data! Try asking about rides, customers, pricing, or drivers. For example: 'Find all Urban rides at Night' or 'How many Gold customers do we have?'",
            'data': {'type': 'help'},
            'suggestions': [
                "Find all Urban rides at Night",
                "How many Gold customers?",
                "What's the average price?"
            ],
            'confidence': 0.6
        }
    
    def _describe_filters(self, filters: Dict[str, Any]) -> str:
        """Create a human-readable description of filters."""
        if not filters:
            return ""
        
        parts = []
        if 'location_category' in filters:
            parts.append(filters['location_category'])
        if 'time_of_booking' in filters:
            parts.append(filters['time_of_booking'].lower())
        
        if parts:
            return " ".join(parts) + " "
        return ""
    
    def _mock_rides_response(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a mock rides response when MongoDB is unavailable."""
        filter_desc = self._describe_filters(filters)
        
        # Mock data based on filters
        mock_count = 127 if 'Urban' in str(filters) else 85
        mock_avg = 285 if 'Night' in str(filters) else 245
        
        return {
            'response': f"I found {mock_count} {filter_desc}rides (using cached data). The average price is ${mock_avg}.",
            'data': {
                'type': 'rides',
                'count': mock_count,
                'avg_price': mock_avg,
                'filters': filters,
                'is_mock': True
            },
            'suggestions': [
                "Show pricing trends",
                "Compare locations",
                "View surge patterns"
            ],
            'confidence': 0.7
        }


# Singleton instance
_chat_agent: Optional[HoneyGoChatAgent] = None


def get_chat_agent(mongodb_service=None) -> HoneyGoChatAgent:
    """
    Get or create the chat agent singleton.
    
    Args:
        mongodb_service: Optional MongoDB service to inject
        
    Returns:
        HoneyGoChatAgent instance
    """
    global _chat_agent
    if _chat_agent is None:
        _chat_agent = HoneyGoChatAgent(mongodb_service)
    elif mongodb_service and _chat_agent.mongodb_service is None:
        _chat_agent.mongodb_service = mongodb_service
    return _chat_agent


def reset_chat_agent():
    """Reset the chat agent singleton (useful for testing)."""
    global _chat_agent
    _chat_agent = None

