"""
HoneyGo Chat Agent - Natural Language Query Interface

Allows users to query the HoneyGo system using natural language.
Uses LangChain to interpret queries and return human-friendly responses.
Enhanced with real-time external data integration.

Author: Safa (Role 4 - LangChain/Agent Engineer)
Created: Dec 3, 2025
Updated: Dec 4, 2025 - Added external data integration
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
    
    def __init__(self, mongodb_service=None, n8n_service=None):
        """
        Initialize the chat agent.
        
        Args:
            mongodb_service: MongoDB service instance for data queries
            n8n_service: N8N service instance for external data (weather, events, traffic)
        """
        self.mongodb_service = mongodb_service
        self.n8n_service = n8n_service
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
        if intent['type'] == 'booking_request':
            result = self._handle_booking_request(message)
        elif intent['type'] == 'rides_query':
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
        
        # Check for booking/action requests first (not supported - we're a query system)
        booking_words = ['book', 'schedule', 'reserve', 'order', 'request a', 'get me a', 'i need a', 'i want a', 'call a', 'hail']
        if any(word in message_lower for word in booking_words):
            intent['type'] = 'booking_request'
            return intent
        
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
    
    def _handle_booking_request(self, message: str) -> Dict[str, Any]:
        """
        Handle booking/action requests with a helpful redirect message.
        
        This chat interface is for QUERYING data, not booking rides.
        """
        return {
            'response': "🚕 I can't book rides directly - I'm a data query assistant! "
                       "To book a ride, please use the HoneyGo app or main interface. "
                       "However, I can help you analyze ride data, pricing trends, "
                       "and customer statistics. Try asking: 'What's the average price for Urban rides?'",
            'data': {
                'type': 'booking_redirect',
                'original_intent': 'booking'
            },
            'suggestions': [
                "What's the average ride price?",
                "Find all Urban rides at Night",
                "How many Gold customers are there?",
                "Show me driver statistics"
            ],
            'confidence': 1.0
        }
    
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
        """Handle queries about pricing with real-time context."""
        
        aggregation = intent.get('aggregation', 'average')
        city = context.get('current_city') if context else None
        
        # Fetch real-time external data for pricing context
        external_data = await self._fetch_external_data(city)
        
        # Query MongoDB if available
        if self.mongodb_service and self.mongodb_service.connected:
            try:
                stats = await self.mongodb_service.get_ride_statistics()
                
                if aggregation == 'average':
                    price = stats.get('average_price', 0)
                    surge = stats.get('average_surge_multiplier', 1.0)
                    response = f"The average price is ${price:.2f} with an average surge multiplier of {surge:.2f}x."
                    
                    # Add real-time pricing factors
                    if external_data['weather']:
                        weather = external_data['weather']
                        weather_multiplier = weather.get('pricing_multiplier', 1.0)
                        if weather_multiplier > 1.0:
                            response += f" Currently, weather conditions ({weather.get('conditions', 'adverse')}) are adding a {weather_multiplier}x multiplier."
                    
                    if external_data['events']:
                        events = external_data['events']
                        if events.get('event_count', 0) > 0:
                            response += f" There are {events['event_count']} events happening, which may increase demand."
                else:
                    price = stats.get('average_price', 0)
                    response = f"Pricing statistics: Average ${price:.2f}"
                
                return {
                    'response': response,
                    'data': {
                        'type': 'pricing',
                        'statistics': stats,
                        'external_factors': external_data,
                        'real_time': True
                    },
                    'suggestions': [
                        "What's the current weather?",
                        "Show events affecting prices",
                        "Compare prices by city"
                    ],
                    'confidence': 0.95
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
    
    async def _fetch_external_data(self, city: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch real-time external data (weather, events, traffic).
        
        Args:
            city: Optional city name for location-specific data
            
        Returns:
            Dict with weather, events, and traffic data
        """
        external_data = {
            'weather': None,
            'events': None,
            'traffic': None
        }
        
        if not city:
            return external_data
        
        # Try N8N service first for real-time data
        if self.n8n_service:
            try:
                weather = await self.n8n_service.get_weather_data(city)
                if weather:
                    external_data['weather'] = weather
                    logger.info(f"✅ Fetched real-time weather for {city}")
            except Exception as e:
                logger.warning(f"N8N weather fetch failed: {e}")
        
        # Fallback to MongoDB cached data
        if not external_data['weather'] and self.mongodb_service:
            try:
                location_category = self._city_to_location_category(city)
                weather = await self.mongodb_service.get_weather_data(location_category)
                if weather:
                    external_data['weather'] = weather.get('data', {})
                    logger.info(f"✅ Fetched cached weather for {city}")
            except Exception as e:
                logger.warning(f"MongoDB weather fetch failed: {e}")
        
        # Try to fetch events data
        if self.n8n_service:
            try:
                events = await self.n8n_service.get_events_data(city)
                if events:
                    external_data['events'] = events
                    logger.info(f"✅ Fetched events for {city}")
            except Exception as e:
                logger.warning(f"Events fetch failed: {e}")
        
        return external_data
    
    def _city_to_location_category(self, city: str) -> str:
        """Map city name to location category."""
        city_lower = city.lower()
        city_map = {
            'new york': 'Urban',
            'nyc': 'Urban',
            'san francisco': 'Urban',
            'chicago': 'Urban',
            'phoenix': 'Suburban',
            'orlando': 'Suburban'
        }
        return city_map.get(city_lower, 'Urban')
    
    async def _handle_general_query(
        self,
        message: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle general/unclassified queries using LLM with real-time data."""
        
        # Fetch external data for context
        city = context.get('current_city') if context else None
        external_data = await self._fetch_external_data(city)
        
        # Check if query is about weather/conditions
        message_lower = message.lower()
        if any(word in message_lower for word in ['weather', 'condition', 'rain', 'storm', 'temperature', 'forecast']):
            return await self._handle_weather_query(message, city, external_data)
        
        if any(word in message_lower for word in ['event', 'concert', 'game', 'happening']):
            return await self._handle_events_query(message, city, external_data)
        
        # Use LLM for complex queries
        if self.is_initialized and self.llm:
            try:
                # Build enhanced context with external data
                context_info = ""
                if external_data['weather']:
                    weather = external_data['weather']
                    context_info += f"\nCurrent weather in {city}: {weather.get('conditions', 'N/A')}, {weather.get('temperature', 'N/A')}°F"
                if external_data['events']:
                    events = external_data['events']
                    context_info += f"\nEvents: {events.get('event_count', 0)} happening"
                
                system_prompt = f"""You are HoneyGo's AI assistant with access to real-time data. 
                Be concise, helpful, and friendly.
                
                HoneyGo features:
                - Dynamic pricing based on demand, weather, and events
                - Customer loyalty tiers (Gold, Silver, Bronze, Regular)
                - Real-time surge pricing during high demand
                - AI-powered pricing explanations
                - Multi-city support (NYC, SF, Chicago, Phoenix, Orlando)
                
                Current Context:{context_info}
                
                Keep responses brief (2-3 sentences max)."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=message)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                return {
                    'response': response.content,
                    'data': {
                        'type': 'general',
                        'external_data': external_data
                    },
                    'suggestions': [
                        "Show current weather",
                        "What events are happening?",
                        "How does pricing work?"
                    ],
                    'confidence': 0.8
                }
            except Exception as e:
                logger.error(f"LLM error in general query: {e}")
        
        # Fallback response
        return {
            'response': "I can help you with HoneyGo data! Try asking about rides, customers, pricing, weather, or events. For example: 'What's the weather like?' or 'Find all Urban rides at Night'",
            'data': {'type': 'help'},
            'suggestions': [
                "What's the current weather?",
                "Find all Urban rides at Night",
                "What events are happening?"
            ],
            'confidence': 0.6
        }
    
    async def _handle_weather_query(
        self,
        message: str,
        city: Optional[str],
        external_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle weather-related queries."""
        weather = external_data.get('weather')
        
        if weather and city:
            conditions = weather.get('conditions', 'Unknown')
            temp = weather.get('temperature', 'N/A')
            pricing_impact = weather.get('pricing_multiplier', 1.0)
            
            response = f"🌤️ Current weather in {city}: {conditions}, {temp}°F. "
            if pricing_impact > 1.0:
                response += f"Weather is affecting prices with a {pricing_impact}x multiplier for driver safety."
            else:
                response += "Weather conditions are favorable - normal pricing applies."
            
            return {
                'response': response,
                'data': {
                    'type': 'weather',
                    'city': city,
                    'weather': weather,
                    'real_time': True
                },
                'suggestions': [
                    "How does weather affect pricing?",
                    "Show pricing for current conditions",
                    "Check traffic conditions"
                ],
                'confidence': 0.95
            }
        else:
            return {
                'response': f"I couldn't fetch current weather data for {city or 'your location'}. Please try again or specify a city.",
                'data': {'type': 'weather', 'error': 'no_data'},
                'suggestions': [
                    "Try: What's the weather in Phoenix?",
                    "Show pricing factors",
                    "View historical rides"
                ],
                'confidence': 0.5
            }
    
    async def _handle_events_query(
        self,
        message: str,
        city: Optional[str],
        external_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle events-related queries."""
        events = external_data.get('events')
        
        if events and city:
            event_count = events.get('event_count', 0)
            major_events = events.get('major_events', [])
            pricing_impact = events.get('pricing_multiplier', 1.0)
            
            if event_count > 0:
                response = f"🎉 There are {event_count} events happening in {city}. "
                if major_events:
                    response += f"Major events: {', '.join(major_events[:2])}. "
                if pricing_impact > 1.0:
                    response += f"High demand expected - prices may increase by {pricing_impact}x."
                else:
                    response += "Standard pricing applies."
            else:
                response = f"No major events currently in {city}. Standard pricing applies."
            
            return {
                'response': response,
                'data': {
                    'type': 'events',
                    'city': city,
                    'events': events,
                    'real_time': True
                },
                'suggestions': [
                    "Show event pricing impact",
                    "Compare demand across cities",
                    "Check weather conditions"
                ],
                'confidence': 0.9
            }
        else:
            return {
                'response': f"I couldn't fetch current events data for {city or 'your location'}. Events may increase ride demand and affect pricing.",
                'data': {'type': 'events', 'error': 'no_data'},
                'suggestions': [
                    "Check weather instead",
                    "Show current prices",
                    "View historical data"
                ],
                'confidence': 0.5
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


def get_chat_agent(mongodb_service=None, n8n_service=None) -> HoneyGoChatAgent:
    """
    Get or create the chat agent singleton.
    
    Args:
        mongodb_service: Optional MongoDB service to inject
        n8n_service: Optional N8N service for external data
        
    Returns:
        HoneyGoChatAgent instance
    """
    global _chat_agent
    if _chat_agent is None:
        _chat_agent = HoneyGoChatAgent(mongodb_service, n8n_service)
    else:
        # Update services if provided
        if mongodb_service and _chat_agent.mongodb_service is None:
            _chat_agent.mongodb_service = mongodb_service
        if n8n_service and _chat_agent.n8n_service is None:
            _chat_agent.n8n_service = n8n_service
    return _chat_agent


def reset_chat_agent():
    """Reset the chat agent singleton (useful for testing)."""
    global _chat_agent
    _chat_agent = None

