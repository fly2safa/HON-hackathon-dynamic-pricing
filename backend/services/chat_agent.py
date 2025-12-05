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
    
    def __init__(self, mongodb_service=None, n8n_service=None, chromadb_service=None):
        """
        Initialize the chat agent.
        
        Args:
            mongodb_service: MongoDB service instance for data queries
            n8n_service: N8N service instance for external data (weather, events, traffic)
            chromadb_service: ChromaDB service instance for RAG/semantic search
        """
        self.mongodb_service = mongodb_service
        self.n8n_service = n8n_service
        self.chromadb_service = chromadb_service
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
        if intent['type'] == 'greeting':
            result = self._handle_greeting()
        elif intent['type'] == 'datetime_query':
            result = self._handle_datetime_query()
        elif intent['type'] == 'booking_request':
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
        
        # Check for greetings first - provide helpful guidance
        greeting_words = ['hi', 'hello', 'hey', 'howdy', 'good morning', 'good afternoon', 'good evening', 'sup', 'yo', 'greetings']
        if any(message_lower.strip() == word or message_lower.startswith(word + ' ') or message_lower.startswith(word + ',') for word in greeting_words):
            intent['type'] = 'greeting'
            return intent
        
        # Check for booking/action requests (not supported - we're a query system)
        booking_words = ['book', 'schedule', 'reserve', 'order', 'request a', 'get me a', 'i need a', 'i want a', 'call a', 'hail']
        if any(word in message_lower for word in booking_words):
            intent['type'] = 'booking_request'
            return intent
        
        # Check for date/time queries - return actual current date
        datetime_words = ['date', 'time', 'today', 'day is it', 'what day', 'current time', 'right now']
        if any(word in message_lower for word in datetime_words):
            intent['type'] = 'datetime_query'
            return intent
        
        # Check for "how does X work/affect" explanation questions - should be general, not data queries
        if any(phrase in message_lower for phrase in ['how does', 'how do', 'what is', 'explain', 'tell me about']):
            # These are explanation questions, let general handler deal with them
            intent['type'] = 'general'
            return intent
        
        # Pricing queries - CHECK FIRST (before rides, so "average price for rides" uses live data)
        if any(word in message_lower for word in ['price', 'pricing', 'cost', 'surge', 'fare']):
            intent['type'] = 'pricing_query'
            
            if 'average' in message_lower or 'avg' in message_lower:
                intent['aggregation'] = 'average'
            elif 'highest' in message_lower or 'max' in message_lower:
                intent['aggregation'] = 'max'
            elif 'lowest' in message_lower or 'min' in message_lower:
                intent['aggregation'] = 'min'
        
        # Rides queries (semantic search for similar rides)
        elif any(word in message_lower for word in ['ride', 'rides', 'trip', 'trips', 'journey', 'similar', 'find']):
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
        
        # Statistics queries
        elif any(word in message_lower for word in ['statistic', 'stats', 'total', 'count', 'how many', 'summary']):
            intent['type'] = 'statistics_query'
        
        # Driver queries
        elif any(word in message_lower for word in ['driver', 'drivers']):
            intent['type'] = 'drivers_query'
            
            if 'active' in message_lower:
                intent['filters']['status'] = 'Active'
        
        return intent
    
    def _handle_greeting(self) -> Dict[str, Any]:
        """
        Handle greetings with a helpful introduction.
        """
        return {
            'response': "Hello! 👋 I'm your HoneyGo data assistant. I can help you explore "
                       "ride statistics, customer data, pricing trends, and more!",
            'data': {
                'type': 'greeting'
            },
            'suggestions': [
                "How many Gold customers?",
                "Find Urban rides at Night",
                "What's the average price?",
                "Show me overall statistics"
            ],
            'confidence': 1.0
        }
    
    def _handle_datetime_query(self) -> Dict[str, Any]:
        """
        Handle date/time queries with the actual current date.
        LLMs don't know the current date, so we provide it directly.
        """
        from datetime import datetime
        now = datetime.now()
        
        # Format: "Friday, December 5, 2025 at 3:45 PM"
        formatted_date = now.strftime("%A, %B %d, %Y")
        formatted_time = now.strftime("%I:%M %p")
        
        return {
            'response': f"📅 Today is {formatted_date}. The current time is {formatted_time}.",
            'data': {
                'type': 'datetime',
                'date': now.strftime("%Y-%m-%d"),
                'time': now.strftime("%H:%M:%S"),
                'day_of_week': now.strftime("%A")
            },
            'suggestions': [
                "What's the average price?",
                "How many Gold customers?",
                "Show me overall statistics"
            ],
            'confidence': 1.0
        }
    
    def _handle_booking_request(self, message: str) -> Dict[str, Any]:
        """
        Handle booking/action requests with a helpful redirect message.
        
        This chat interface is for QUERYING data, not booking rides.
        """
        return {
            'response': "🚕 I can't book rides directly - I'm a data query assistant! "
                       "To book a ride, please use the HoneyGo app or main interface. "
                       "However, I can help you analyze ride data, pricing trends, "
                       "and customer statistics.",
            'data': {
                'type': 'booking_redirect',
                'original_intent': 'booking'
            },
            'suggestions': [
                "How many Gold customers are there?",
                "What's the average surge multiplier?",
                "Show me overall statistics",
                "How many active drivers?"
            ],
            'confidence': 1.0
        }
    
    async def _query_chromadb_similar(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query ChromaDB for similar rides using semantic search (RAG).
        
        Args:
            query: Natural language query
            n_results: Number of results to return
            
        Returns:
            List of similar rides with similarity scores
        """
        if not self.chromadb_service or not self.chromadb_service.connected:
            return []
        
        try:
            results = await self.chromadb_service.query_similar_rides(
                query=query,
                n_results=n_results
            )
            logger.info(f"🔍 ChromaDB RAG: Found {len(results)} similar rides")
            return results
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
            return []
    
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
        
        # First, try ChromaDB semantic search (RAG)
        chromadb_results = await self._query_chromadb_similar(message, n_results=5)
        
        if chromadb_results and len(chromadb_results) > 0:
            # Use ChromaDB results for semantic search
            avg_price = sum(r.get('metadata', {}).get('historical_cost_of_ride', 0) for r in chromadb_results) / len(chromadb_results)
            avg_similarity = sum(r.get('similarity', 0) for r in chromadb_results) / len(chromadb_results)
            
            # Build response with RAG context
            response = f"Using semantic search (RAG), I found {len(chromadb_results)} similar rides. "
            response += f"Average price for similar rides: ${avg_price:.2f} "
            response += f"(similarity: {avg_similarity:.0%})"
            
            # Include top result details
            top_result = chromadb_results[0]
            meta = top_result.get('metadata', {})
            if meta:
                response += f"\n\nTop match: {meta.get('location_category', 'Unknown')} {meta.get('vehicle_type', 'Standard')} ride "
                response += f"at {meta.get('time_of_booking', 'Unknown')} - ${meta.get('historical_cost_of_ride', 0):.2f}"
            
            return {
                'response': response,
                'data': {
                    'type': 'rides_rag',
                    'source': 'chromadb',
                    'count': len(chromadb_results),
                    'avg_price': round(avg_price, 2),
                    'avg_similarity': round(avg_similarity, 2),
                    'top_results': chromadb_results[:3]
                },
                'suggestions': [
                    "Find Urban rides at Night",
                    "Show Premium vehicle rides",
                    "What's the average price?"
                ],
                'confidence': avg_similarity
            }
        
        # Fallback to MongoDB if ChromaDB has no results
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
                            "What's the average price?",
                            "Find night rides",
                            "How many active drivers?"
                        ],
                        'confidence': 0.9
                    }
                else:
                    # No data in MongoDB - return mock with explanation
                    logger.info("No rides in MongoDB, using mock data")
                    return self._mock_rides_response(filters, db_connected=True)
            except Exception as e:
                logger.error(f"Error querying rides: {e}")
        
        # Fallback response (mock data - backend/DB not available)
        return self._mock_rides_response(filters, db_connected=False)
    
    async def _handle_customers_query(
        self,
        message: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries about customers."""
        
        message_lower = message.lower()
        
        # Check for unsupported customer queries
        unsupported_terms = ['spend', 'spending', 'revenue', 'earned', 'retention', 'satisfaction', 'rating']
        if any(term in message_lower for term in unsupported_terms):
            return {
                'response': "I can tell you about customer counts by loyalty tier, but I don't have data on spending or retention yet. Try asking: 'How many Gold customers are there?'",
                'data': {'type': 'customers', 'unsupported_query': True},
                'suggestions': [
                    "How many Gold customers?",
                    "How many Silver customers?",
                    "Show me overall statistics"
                ],
                'confidence': 0.6
            }
        
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
                "How many Gold customers?",
                "How many Silver customers?",
                "Show me overall statistics"
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
        context_weather = context.get('current_weather') if context else None
        
        # Fetch real-time external data for pricing context
        external_data = await self._fetch_external_data(city, context_weather)
        
        # Query MongoDB if available
        if self.mongodb_service and self.mongodb_service.connected:
            try:
                stats = await self.mongodb_service.get_ride_statistics()
                
                # Check if we have real data (not zeros)
                price = stats.get('average_price', 0)
                surge = stats.get('average_surge_multiplier', 0)
                
                if price > 0:  # Only use MongoDB data if we have real data
                    if aggregation == 'average':
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
                            "What events are happening?",
                            "Find Urban rides at Night"
                        ],
                        'confidence': 0.95
                    }
                else:
                    # No real data in MongoDB - return mock with explanation
                    logger.info("No pricing data in MongoDB, using mock data")
                    return {
                        'response': "📡 Connected to database, but no pricing data exists yet. "
                                   "Reverting to demo data:\n\n"
                                   "The average ride price is $32.50 with a typical surge multiplier of 1.25x during peak hours.",
                        'data': {
                            'type': 'pricing',
                            'avg_price': 32.50,
                            'avg_surge': 1.25,
                            'is_mock': True,
                            'db_connected': True
                        },
                        'suggestions': [
                            "Find Urban rides at Night",
                            "How many active drivers?",
                            "Show me overall statistics"
                        ],
                        'confidence': 0.75
                    }
            except Exception as e:
                logger.error(f"Error querying pricing: {e}")
        
        # Fallback mock response (backend/DB not available)
        return {
            'response': "The average ride price is $32.50 with a typical surge multiplier of 1.25x during peak hours. (Using cached data)",
            'data': {
                'type': 'pricing',
                'avg_price': 32.50,
                'avg_surge': 1.25,
                'is_mock': True
            },
            'suggestions': [
                "Find Urban rides at Night",
                "How many active drivers?",
                "Show me overall statistics"
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
                
                # Check if we have real data
                total_decisions = ride_stats.get('total_pricing_decisions', 0)
                avg_price = ride_stats.get('average_price', 0)
                
                if total_decisions > 0 or avg_price > 0:
                    response = f"📊 HoneyGo Statistics:\n"
                    response += f"• Total pricing decisions: {total_decisions}\n"
                    response += f"• Total revenue: ${ride_stats.get('total_revenue', 0):,.2f}\n"
                    response += f"• Average price: ${avg_price:.2f}\n"
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
                            "How many active drivers?",
                            "How many Gold customers?",
                            "Find Urban rides at Night"
                        ],
                        'confidence': 0.95
                    }
                else:
                    # No real data - return mock with explanation
                    logger.info("No statistics in MongoDB, using mock data")
                    return {
                        'response': "📡 Connected to database, but no statistics exist yet. "
                                   "Reverting to demo data:\n\n"
                                   "📊 HoneyGo has processed over 1,000 rides with $32,500 in total revenue. "
                                   "Average price is $32.50 with 50 active drivers maintaining a 4.7⭐ average rating.",
                        'data': {
                            'type': 'statistics',
                            'is_mock': True,
                            'db_connected': True
                        },
                        'suggestions': [
                            "How many active drivers?",
                            "How many Gold customers?",
                            "What's the average price?"
                        ],
                        'confidence': 0.7
                    }
            except Exception as e:
                logger.error(f"Error querying statistics: {e}")
        
        # Fallback mock response (backend/DB not available)
        return {
            'response': "📊 HoneyGo has processed over 1,000 rides with $32,500 in total revenue. "
                       "Average price is $32.50 with 50 active drivers maintaining a 4.7⭐ average rating. (Using cached data)",
            'data': {'type': 'statistics', 'is_mock': True},
            'suggestions': [
                "How many active drivers?",
                "How many Gold customers?",
                "What's the average price?"
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
                    
                    return {
                        'response': response,
                        'data': {
                            'type': 'drivers',
                            'count': count,
                            'avg_rating': round(avg_rating, 1)
                        },
                        'suggestions': [
                            "Show me overall statistics",
                            "Find Urban rides",
                            "How many Gold customers?"
                        ],
                        'confidence': 0.9
                    }
                else:
                    # No drivers in MongoDB - return mock with explanation
                    logger.info("No drivers in MongoDB, using mock data")
                    return {
                        'response': "📡 Connected to database, but no driver data exists yet. "
                                   "Reverting to demo data:\n\n"
                                   "There are 50 active drivers with an average rating of 4.7⭐. "
                                   "Top performers earn over $300 per day.",
                        'data': {
                            'type': 'drivers',
                            'count': 50,
                            'avg_rating': 4.7,
                            'is_mock': True,
                            'db_connected': True
                        },
                        'suggestions': [
                            "Show me overall statistics",
                            "How many Gold customers?",
                            "What's the average price?"
                        ],
                        'confidence': 0.75
                    }
            except Exception as e:
                logger.error(f"Error querying drivers: {e}")
        
        # Fallback mock response (backend/DB not available)
        return {
            'response': "There are 50 active drivers with an average rating of 4.7⭐. "
                       "Top performers earn over $300 per day. (Using cached data)",
            'data': {
                'type': 'drivers',
                'count': 50,
                'avg_rating': 4.7,
                'is_mock': True
            },
            'suggestions': [
                "Show me overall statistics",
                "How many Gold customers?",
                "What's the average price?"
            ],
            'confidence': 0.75
        }
    
    async def _fetch_external_data(self, city: Optional[str] = None, context_weather: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch real-time external data (weather, events, traffic).
        
        Args:
            city: Optional city name for location-specific data
            context_weather: Optional weather data passed from frontend (live weather)
            
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
        
        # PRIORITY 1: Use weather from frontend context (live weather from UI)
        if context_weather:
            external_data['weather'] = {
                'conditions': context_weather.get('conditions', 'Unknown'),
                'temperature': context_weather.get('temperature', 0),
                'weather_type': context_weather.get('weather_type', 'clear'),
                'pricing_multiplier': 1.0 if context_weather.get('weather_type') in ['clear', 'clouds'] else 1.1,
                'is_live': context_weather.get('is_real_data', False)
            }
            logger.info(f"✅ Using live weather from frontend for {city}: {external_data['weather']['conditions']}, {external_data['weather']['temperature']}°F")
            return external_data  # Skip other fetches since we have live data
        
        # Try N8N service for real-time data (fallback)
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
        
        # Final fallback: mock weather data for demo
        if not external_data['weather'] and city:
            mock_weather = self._get_mock_weather(city)
            external_data['weather'] = mock_weather
            logger.info(f"📋 Using mock weather for {city}")
        
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
    
    def _extract_city_from_message(self, message: str) -> Optional[str]:
        """Extract city name from user message."""
        message_lower = message.lower()
        
        # List of supported cities and their variations
        city_keywords = {
            'phoenix': 'Phoenix',
            'new york': 'New York',
            'nyc': 'New York',
            'san francisco': 'San Francisco',
            'sf': 'San Francisco',
            'chicago': 'Chicago',
            'orlando': 'Orlando'
        }
        
        for keyword, city_name in city_keywords.items():
            if keyword in message_lower:
                return city_name
        
        return None
    
    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """Get mock weather data for demo purposes."""
        import random
        
        # Realistic mock weather for each city
        city_weather = {
            'Phoenix': {'conditions': 'Clear', 'temperature': 72, 'pricing_multiplier': 1.0},
            'New York': {'conditions': 'Cloudy', 'temperature': 45, 'pricing_multiplier': 1.0},
            'San Francisco': {'conditions': 'Foggy', 'temperature': 58, 'pricing_multiplier': 1.1},
            'Chicago': {'conditions': 'Windy', 'temperature': 38, 'pricing_multiplier': 1.1},
            'Orlando': {'conditions': 'Partly Cloudy', 'temperature': 78, 'pricing_multiplier': 1.0},
        }
        
        # Get city-specific weather or generate random
        if city in city_weather:
            weather = city_weather[city].copy()
        else:
            weather = {
                'conditions': random.choice(['Clear', 'Cloudy', 'Partly Cloudy']),
                'temperature': random.randint(40, 85),
                'pricing_multiplier': 1.0
            }
        
        weather['is_mock'] = True
        return weather
    
    async def _handle_general_query(
        self,
        message: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle general/unclassified queries using LLM with real-time data."""
        
        # Get context city (what's selected in UI dropdown)
        context_city = context.get('current_city') if context else None
        context_weather = context.get('current_weather') if context else None
        
        # DEBUG
        logger.info(f"🔍 DEBUG: context_city={context_city}, context_weather={context_weather}")
        
        # Try to extract city from message (e.g., "What's the weather in NY?")
        message_city = self._extract_city_from_message(message)
        logger.info(f"🔍 DEBUG: message_city={message_city}")
        
        # Use message city if specified, otherwise fall back to context city
        city = message_city or context_city
        
        # IMPORTANT: Only use context_weather if the city matches the context city
        # If user asks about a different city, don't use the cached weather
        use_context_weather = context_weather if (city == context_city or not message_city) else None
        logger.info(f"🔍 DEBUG: city={city}, use_context_weather={use_context_weather is not None}")
        
        # Fetch external data for context
        external_data = await self._fetch_external_data(city, use_context_weather)
        
        # Check if query is about traffic
        message_lower = message.lower()
        if 'traffic' in message_lower:
            return await self._handle_traffic_query(message, city, external_data)
        
        # Check if query is about weather (but not traffic conditions)
        if any(word in message_lower for word in ['weather', 'rain', 'storm', 'temperature', 'forecast', 'sunny', 'cloudy']):
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
    
    async def _handle_traffic_query(
        self,
        message: str,
        city: Optional[str],
        external_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle traffic-related queries."""
        # Generate realistic traffic based on time of day
        from datetime import datetime
        current_hour = datetime.now().hour
        
        # Traffic patterns: rush hours have heavy traffic
        if 7 <= current_hour <= 9 or 16 <= current_hour <= 19:
            traffic_level = "Heavy"
            multiplier = 1.3
            description = "Rush hour traffic detected"
        elif 10 <= current_hour <= 15:
            traffic_level = "Moderate"
            multiplier = 1.1
            description = "Normal daytime traffic"
        else:
            traffic_level = "Light"
            multiplier = 1.0
            description = "Low traffic volume"
        
        response = f"🚗 Traffic in {city or 'your area'}: {traffic_level}. {description}. "
        if multiplier > 1.0:
            response += f"Expect a {multiplier}x pricing adjustment for longer ETAs."
        else:
            response += "Standard pricing applies with quick pickup times."
        
        return {
            'response': response,
            'data': {
                'type': 'traffic',
                'city': city,
                'traffic_level': traffic_level,
                'multiplier': multiplier
            },
            'suggestions': [
                "Check weather conditions",
                "What events are happening?",
                "Calculate ride price"
            ],
            'confidence': 0.9
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
    
    def _mock_rides_response(self, filters: Dict[str, Any], db_connected: bool = False) -> Dict[str, Any]:
        """Generate a mock rides response when MongoDB has no data or is unavailable."""
        filter_desc = self._describe_filters(filters)
        
        # Mock data based on filters - realistic ride prices
        mock_count = 127 if 'Urban' in str(filters) else 85
        
        # Realistic pricing: Night rides have surge, Urban is slightly higher
        base_price = 28.50  # Base average ride price
        if 'Night' in str(filters):
            mock_avg = round(base_price * 1.35, 2)  # 35% night surge = $38.48
        elif 'Urban' in str(filters):
            mock_avg = round(base_price * 1.15, 2)  # 15% urban premium = $32.78
        else:
            mock_avg = base_price
        
        # Different message based on DB connection status
        if db_connected:
            response = (f"📡 Connected to database, but no {filter_desc}ride data exists yet. "
                       f"Reverting to demo data:\n\n"
                       f"I found {mock_count} {filter_desc}rides. The average price is ${mock_avg}.")
        else:
            response = f"I found {mock_count} {filter_desc}rides. The average price is ${mock_avg}. (Using cached data)"
        
        return {
            'response': response,
            'data': {
                'type': 'rides',
                'count': mock_count,
                'avg_price': mock_avg,
                'filters': filters,
                'is_mock': True,
                'db_connected': db_connected
            },
            'suggestions': [
                "What's the average price?",
                "How many active drivers?",
                "Show me overall statistics"
            ],
            'confidence': 0.7
        }


# Singleton instance
_chat_agent: Optional[HoneyGoChatAgent] = None


def get_chat_agent(mongodb_service=None, n8n_service=None, chromadb_service=None) -> HoneyGoChatAgent:
    """
    Get or create the chat agent singleton.
    
    Args:
        mongodb_service: Optional MongoDB service to inject
        n8n_service: Optional N8N service for external data
        chromadb_service: Optional ChromaDB service for RAG queries
        
    Returns:
        HoneyGoChatAgent instance
    """
    global _chat_agent
    if _chat_agent is None:
        _chat_agent = HoneyGoChatAgent(mongodb_service, n8n_service, chromadb_service)
    else:
        # Update services if provided
        if mongodb_service and _chat_agent.mongodb_service is None:
            _chat_agent.mongodb_service = mongodb_service
        if n8n_service and _chat_agent.n8n_service is None:
            _chat_agent.n8n_service = n8n_service
        if chromadb_service and _chat_agent.chromadb_service is None:
            _chat_agent.chromadb_service = chromadb_service
    return _chat_agent


def reset_chat_agent():
    """Reset the chat agent singleton (useful for testing)."""
    global _chat_agent
    _chat_agent = None

