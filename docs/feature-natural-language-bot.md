# Feature: Natural Language Query Bot 🤖

## Overview

Add a conversational AI interface that allows users to query the HoneyGo system using natural language (text or voice). The LangChain agent interprets queries and returns human-friendly responses.

**Owner:** Safa (Primary - LangChain/Backend), Dari (Backend API Support)  
**Priority:** High (Demo Differentiator)  
**Estimated Effort:** 3-4 hours

> **Note:** Voice features (🎤 input, 🔊 output) are handled separately.
> See: [feature-speak-reasoning.md](./feature-speak-reasoning.md)

---

## User Stories

### Story 1: Text-Based Query
```
As a user,
I want to ask questions in plain English,
So that I can get insights without knowing database syntax.
```

**Example:**
> User: "Find all Urban rides at Night"
> Bot: "I found 127 Urban night rides. Average price: $285. Highest surge was 1.8x."

### Story 2: Follow-up Questions
```
As a user,
I want suggested follow-up questions,
So that I can explore data without knowing what to ask.
```

**Example:**
> Bot suggests: "Compare with other cities" → User clicks → Bot responds

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ChatBot Component                                   │   │
│  │  - Text input field                                  │   │
│  │  - Voice input button (🎤)                          │   │
│  │  - Chat history display                              │   │
│  │  - Voice output toggle (🔊)                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│                    POST /api/v1/chat                        │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  /api/v1/chat Endpoint                               │   │
│  │  - Receives: { message: string, context?: object }   │   │
│  │  - Returns: { response: string, data?: object }      │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  LangChain Conversational Agent                      │   │
│  │  - Intent Classification                             │   │
│  │  - Query Parameter Extraction                        │   │
│  │  - Tool Selection & Execution                        │   │
│  │  - Natural Language Response Generation              │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                               │
│                    ┌─────────┴─────────┐                    │
│                    ▼                   ▼                     │
│              ┌──────────┐       ┌──────────┐                │
│              │ MongoDB  │       │ ChromaDB │                │
│              │ (Facts)  │       │ (Context)│                │
│              └──────────┘       └──────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## Supported Query Types

### 1. Data Queries (MongoDB)
| User Says | Bot Does | Example Response |
|-----------|----------|------------------|
| "Find all Urban rides at Night" | Query rides collection | "Found 127 rides, avg price $285" |
| "How many Gold customers?" | Query customers collection | "You have 45 Gold tier customers" |
| "Show surge pricing history" | Query pricing_decisions | "Average surge: 1.15x, max: 2.1x" |
| "What's the demand in Phoenix?" | Query by city | "Phoenix has moderate demand (1.1x)" |

### 2. Analytics Queries
| User Says | Bot Does | Example Response |
|-----------|----------|------------------|
| "Compare prices across cities" | Aggregation query | "NYC is highest ($320), Phoenix lowest ($185)" |
| "What's the average driver earnings?" | Calculate from data | "Drivers earn $240 avg per ride (80%)" |
| "Show pricing trends" | Time-series analysis | "Prices up 15% during evening hours" |

### 3. Contextual Queries (ChromaDB)
| User Says | Bot Does | Example Response |
|-----------|----------|------------------|
| "How did we handle concert pricing before?" | Semantic search | "Similar events used 20% surge successfully" |
| "What's HON's policy on surge?" | Query knowledge base | "Gold customers get surge protection..." |

### 4. Action Requests
| User Says | Bot Does | Example Response |
|-----------|----------|------------------|
| "Calculate price for a ride from downtown to airport" | Trigger pricing | "Recommended price: $45, surge 1.0x" |
| "What if demand doubles?" | Scenario analysis | "Price would increase to $58 (1.3x surge)" |

---

## API Specification

### Endpoint: POST /api/v1/chat

**Request:**
```typescript
interface ChatRequest {
  message: string;           // User's natural language query
  conversation_id?: string;  // For multi-turn conversations
  context?: {
    current_city?: string;   // Current selected city
    current_ride?: string;   // Current selected ride
  };
}
```

**Response:**
```typescript
interface ChatResponse {
  response: string;          // Natural language response
  data?: {
    type: 'rides' | 'customers' | 'pricing' | 'analytics';
    items?: any[];           // Query results if applicable
    chart_data?: any;        // For visualization
  };
  suggestions?: string[];    // Follow-up question suggestions
  confidence: number;        // 0-1 confidence score
}
```

**Example:**
```json
// Request
{
  "message": "Find all Urban rides at Night",
  "context": { "current_city": "New York" }
}

// Response
{
  "response": "I found 127 Urban night rides in New York. The average price is $285, with surge multipliers ranging from 1.0x to 1.8x. Would you like to see the pricing breakdown?",
  "data": {
    "type": "rides",
    "items": [...],
    "summary": {
      "count": 127,
      "avg_price": 285,
      "max_surge": 1.8
    }
  },
  "suggestions": [
    "Show pricing trends",
    "Compare with other cities",
    "What causes the highest surge?"
  ],
  "confidence": 0.92
}
```

---

## Implementation Steps

### Phase 1: Backend Chat Endpoint (2 hours)

**File:** `backend/routers/chat.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
from services.langchain_service import get_chat_agent

router = APIRouter(prefix="/api/v1", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    data: Optional[dict] = None
    suggestions: Optional[List[str]] = None
    confidence: float = 0.8

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process natural language query and return response.
    """
    try:
        agent = get_chat_agent()
        result = await agent.process_query(
            message=request.message,
            context=request.context
        )
        return ChatResponse(
            response=result['response'],
            data=result.get('data'),
            suggestions=result.get('suggestions'),
            confidence=result.get('confidence', 0.8)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### Phase 2: LangChain Chat Agent (2 hours)

**File:** `backend/services/chat_agent.py`

```python
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

class HoneyGoChatAgent:
    """
    Conversational agent for natural language queries.
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Define tools for different query types
        self.tools = [
            Tool(
                name="Query_Rides",
                func=self.query_rides,
                description="Query ride data. Use for questions about rides, trips, locations, times."
            ),
            Tool(
                name="Query_Customers",
                func=self.query_customers,
                description="Query customer data. Use for questions about customers, loyalty tiers, ratings."
            ),
            Tool(
                name="Query_Pricing",
                func=self.query_pricing,
                description="Query pricing decisions. Use for questions about prices, surge, discounts."
            ),
            Tool(
                name="Calculate_Price",
                func=self.calculate_price,
                description="Calculate a new price. Use when user wants to price a ride."
            ),
            Tool(
                name="Search_Knowledge",
                func=self.search_knowledge,
                description="Search HON knowledge base. Use for policy questions, best practices."
            ),
        ]
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
    
    async def process_query(self, message: str, context: dict = None) -> dict:
        """Process a natural language query."""
        
        # Add context to the query if provided
        if context:
            context_str = f"\nContext: City={context.get('current_city', 'Any')}"
            message = message + context_str
        
        # Run agent
        response = self.agent.run(message)
        
        # Extract suggestions based on response
        suggestions = self._generate_suggestions(message, response)
        
        return {
            'response': response,
            'suggestions': suggestions,
            'confidence': 0.85
        }
    
    def query_rides(self, query: str) -> str:
        """Query rides collection based on natural language."""
        # Parse query and build MongoDB filter
        # ... implementation
        pass
    
    def query_customers(self, query: str) -> str:
        """Query customers collection."""
        pass
    
    def query_pricing(self, query: str) -> str:
        """Query pricing decisions."""
        pass
    
    def calculate_price(self, params: str) -> str:
        """Calculate price for a ride."""
        pass
    
    def search_knowledge(self, query: str) -> str:
        """Search ChromaDB knowledge base."""
        pass
    
    def _generate_suggestions(self, query: str, response: str) -> List[str]:
        """Generate follow-up question suggestions."""
        return [
            "Show me more details",
            "Compare with other cities",
            "What's the trend over time?"
        ]

# Singleton
_chat_agent = None

def get_chat_agent():
    global _chat_agent
    if _chat_agent is None:
        _chat_agent = HoneyGoChatAgent()
    return _chat_agent
```

---

### Phase 3: Frontend Chat Component (1.5 hours)

**File:** `frontend/components/ChatBot.tsx`

```typescript
'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'bot';
  content: string;
  data?: any;
  suggestions?: string[];
}

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      
      const data = await response.json();
      
      // Add bot response
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: data.response,
        data: data.data,
        suggestions: data.suggestions
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px] bg-gray-900 rounded-xl border border-gray-700">
      {/* Header */}
      <div className="flex items-center gap-2 p-4 border-b border-gray-700">
        <MessageCircle className="text-[#FF6A13]" size={24} />
        <h3 className="font-semibold text-white">HoneyGo Assistant</h3>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-8">
            <p className="text-lg">👋 Hi! I'm your HoneyGo Assistant.</p>
            <p className="text-sm mt-2">Try asking:</p>
            <div className="mt-4 space-y-2">
              {[
                "Find all Urban rides at Night",
                "How many Gold customers do we have?",
                "What's the average surge in New York?",
                "Calculate price for a 10km ride"
              ].map((suggestion, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(suggestion)}
                  className="block w-full text-left px-4 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 text-sm"
                >
                  "{suggestion}"
                </button>
              ))}
            </div>
          </div>
        )}
        
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-xl p-3 ${
                msg.role === 'user'
                  ? 'bg-[#FF6A13] text-white'
                  : 'bg-gray-800 text-gray-100'
              }`}
            >
              {msg.content}
              
              {/* Suggestions */}
              {msg.suggestions && (
                <div className="mt-3 pt-3 border-t border-gray-600 space-y-1">
                  <p className="text-xs text-gray-400">Follow-up:</p>
                  {msg.suggestions.map((s, i) => (
                    <button
                      key={i}
                      onClick={() => sendMessage(s)}
                      className="block text-xs text-[#FF6A13] hover:underline"
                    >
                      → {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-xl p-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input - Text only (no voice) */}
      <div className="p-4 border-t border-gray-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage(input)}
            placeholder="Ask me anything..."
            className="flex-1 bg-gray-800 border border-gray-600 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-[#FF6A13]"
          />
          
          <button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || isLoading}
            className="p-3 bg-[#FF6A13] rounded-xl hover:bg-[#e55a0a] disabled:opacity-50"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## Demo Script

### For Dari's Presentation:

**Scene 1: Introduction**
> "One unique feature of HoneyGo is our natural language interface. Instead of complex dashboards, users can simply ask questions."

**Scene 2: Demo**
> *Type:* "Find all Urban rides at Night"
> *Bot responds with data*
> "As you can see, the AI understood my query, searched MongoDB, and gave me a human-friendly answer."

**Scene 3: Follow-up**
> *Click a suggestion:* "Compare with other cities"
> "The bot maintains context and can answer follow-up questions."

**Scene 4: Explore**
> *Try different queries:* "How many Gold customers?" or "What's the average surge?"
> "The bot can handle a wide variety of data questions."

---

## Timeline

| Task | Owner | Time | Day |
|------|-------|------|-----|
| Backend /chat endpoint | Dari | 1 hour | Dec 3-4 |
| LangChain chat agent | Safa | 1.5 hours | Dec 3-4 |
| Frontend ChatBot component | Safa | 1.5 hours | Dec 3-4 |
| Testing & polish | Safa | 1 hour | Dec 4 |
| **Total** | | **5 hours** | |

> **Note:** Jason is handling the 🔊 Speaker feature separately (30 min).

---

## Success Criteria

- [ ] User can type a natural language query
- [ ] Bot returns human-friendly response
- [ ] Response includes relevant data
- [ ] Suggestions for follow-up questions appear
- [ ] Chat maintains conversation context
- [ ] Works with MongoDB queries (rides, customers, pricing)

---

## Notes

- This feature significantly enhances the demo experience
- Shows LangChain capabilities beyond just pricing
- Differentiates from other teams
- Aligns with Honeywell's vision of AI-powered tools

---

## Future Enhancements (If Time Permits)

### 🎤 Voice Input for Chat Bot
**Status:** Planned for future / stretch goal

The chat bot currently supports text input. As a future enhancement, we could add voice input:

```typescript
// Add mic button to ChatBot.tsx
<button onClick={startVoiceInput}>
  🎤
</button>

const startVoiceInput = () => {
  const recognition = new (window as any).webkitSpeechRecognition();
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    sendMessage(transcript);  // Send voice query to bot
  };
  recognition.start();
};
```

**Demo Script (if implemented):**
> *Click mic button* 🎤
> *Speak:* "How many Gold customers do we have?"
> *Bot responds with answer*

**Talking Point for Presentation:**
> "The chat interface currently supports text queries. As a future enhancement, we plan to add voice input, enabling fully conversational interaction with the AI assistant."

### 🔊 Voice Output for Bot Responses
We could also add text-to-speech for bot responses, similar to the AI Reasoning speaker.

---

**Document for:** Safa (Primary), Dari (Backend API)  
**Created:** Dec 3, 2025  
**Priority:** High

