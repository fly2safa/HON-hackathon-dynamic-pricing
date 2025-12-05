"""
Chat Router - Natural Language Query Interface

Handles conversational AI queries for the HoneyGo system.
Users can query rides, customers, pricing, and statistics using natural language.

Author: Dari (Role 3 - Backend/FastAPI Engineer)
Created: Dec 3, 2025
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

from services.chat_agent import get_chat_agent
from services import mongodb_service as mongo_module
from services import chromadb_service as chroma_module
from services.n8n_service import N8nService

logger = logging.getLogger(__name__)

# Initialize N8N service for external data
n8n_service = N8nService()

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
    responses={
        200: {"description": "Successful response"},
        500: {"description": "Internal server error"}
    }
)


class ChatRequest(BaseModel):
    """
    Request model for chat queries.
    
    Attributes:
        message: The user's natural language query
        conversation_id: Optional ID for multi-turn conversations
        context: Optional context information (current city, ride, etc.)
    """
    message: str = Field(..., description="User's natural language query", min_length=1)
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context tracking")
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional context like current_city or current_ride"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Find all Urban rides at Night",
                "context": {
                    "current_city": "New York"
                }
            }
        }


class ChatResponse(BaseModel):
    """
    Response model for chat queries.
    
    Attributes:
        response: Natural language response from the AI
        data: Optional structured data (query results, statistics, etc.)
        suggestions: Follow-up question suggestions
        confidence: Confidence score (0-1) of the response
    """
    response: str = Field(..., description="Natural language response")
    data: Optional[Dict[str, Any]] = Field(None, description="Structured data if applicable")
    suggestions: Optional[List[str]] = Field(None, description="Follow-up question suggestions")
    confidence: float = Field(0.8, description="Confidence score between 0 and 1", ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I found 127 Urban night rides. The average price is $285.",
                "data": {
                    "type": "rides",
                    "count": 127,
                    "avg_price": 285,
                    "filters": {
                        "location_category": "Urban",
                        "time_of_booking": "Night"
                    }
                },
                "suggestions": [
                    "Show pricing trends",
                    "Compare with other cities",
                    "What causes the highest surge?"
                ],
                "confidence": 0.92
            }
        }


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process natural language query and return human-friendly response.
    
    This endpoint allows users to query the HoneyGo system using natural language.
    The AI agent interprets the query, fetches relevant data, and returns a
    conversational response with suggestions for follow-up questions.
    
    **Supported Query Types:**
    - Rides: "Find all Urban rides at Night"
    - Customers: "How many Gold customers do we have?"
    - Pricing: "What's the average surge multiplier?"
    - Statistics: "Show me overall statistics"
    - Drivers: "How many active drivers are there?"
    - General: "How does dynamic pricing work?"
    
    Args:
        request: ChatRequest with user message and optional context
        
    Returns:
        ChatResponse with natural language response and structured data
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        logger.info(f"📝 Processing chat query: '{request.message[:50]}...'")
        
        # Get the chat agent with MongoDB, N8N, and ChromaDB services
        agent = get_chat_agent(
            mongodb_service=mongo_module.mongodb_service,
            n8n_service=n8n_service,
            chromadb_service=chroma_module.chromadb_service
        )
        
        # Process the query
        result = await agent.process_query(
            message=request.message,
            context=request.context
        )
        
        # Build response
        response = ChatResponse(
            response=result.get('response', 'I could not process that query.'),
            data=result.get('data'),
            suggestions=result.get('suggestions', []),
            confidence=result.get('confidence', 0.5)
        )
        
        logger.info(f"✅ Chat query processed successfully (confidence: {response.confidence:.2f})")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error processing chat query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat query: {str(e)}"
        )


@router.get("/health", tags=["chat", "health"])
async def chat_health_check() -> Dict[str, Any]:
    """
    Health check for chat service.
    
    Returns information about the chat service status, including:
    - Whether LangChain is initialized
    - Whether MongoDB connection is available
    - Service version
    
    Returns:
        Dict with health status information
    """
    try:
        agent = get_chat_agent(
            mongodb_service=mongo_module.mongodb_service,
            chromadb_service=chroma_module.chromadb_service
        )
        
        return {
            "status": "healthy",
            "service": "chat",
            "llm_initialized": agent.is_initialized,
            "mongodb_available": (
                mongo_module.mongodb_service is not None 
                and mongo_module.mongodb_service.connected
            ),
            "message": "Chat service is operational"
        }
    except Exception as e:
        logger.error(f"Chat health check failed: {e}")
        return {
            "status": "degraded",
            "service": "chat",
            "llm_initialized": False,
            "mongodb_available": False,
            "error": str(e),
            "message": "Chat service is running in fallback mode"
        }


@router.get("/capabilities", tags=["chat"])
async def get_chat_capabilities() -> Dict[str, Any]:
    """
    Get information about chat capabilities and example queries.
    
    Returns:
        Dict with supported query types and examples
    """
    return {
        "service": "HoneyGo Chat AI",
        "description": "Natural language interface for querying HoneyGo data",
        "capabilities": [
            {
                "type": "rides_query",
                "description": "Query historical ride data",
                "examples": [
                    "Find all Urban rides at Night",
                    "Show me rides from New York",
                    "What rides happened in the morning?"
                ]
            },
            {
                "type": "customers_query",
                "description": "Query customer information",
                "examples": [
                    "How many Gold customers do we have?",
                    "Show Silver tier customers",
                    "What's the customer breakdown by loyalty?"
                ]
            },
            {
                "type": "pricing_query",
                "description": "Analyze pricing and surge data",
                "examples": [
                    "What's the average ride price?",
                    "Show me the highest surge multiplier",
                    "What's the pricing trend?"
                ]
            },
            {
                "type": "statistics_query",
                "description": "Get overall system statistics",
                "examples": [
                    "Show me overall statistics",
                    "What's the total revenue?",
                    "How many rides have we done?"
                ]
            },
            {
                "type": "drivers_query",
                "description": "Query driver information",
                "examples": [
                    "How many active drivers are there?",
                    "What's the average driver rating?",
                    "Show top rated drivers"
                ]
            },
            {
                "type": "general",
                "description": "General questions about HoneyGo",
                "examples": [
                    "How does dynamic pricing work?",
                    "What cities do you support?",
                    "Tell me about HoneyGo"
                ]
            }
        ],
        "features": [
            "Natural language understanding",
            "Intent classification",
            "MongoDB integration",
            "Follow-up suggestions",
            "Multi-turn conversations (planned)",
            "Voice input support (frontend)",
            "Voice output support (frontend)"
        ]
    }

