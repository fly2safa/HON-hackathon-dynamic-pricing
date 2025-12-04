# HoneyGo Demo Cheat Sheet 🍯🚗

**Demo Date:** December 5, 2024  
**Presenter:** Safa (Role 4 - LangChain/AI Agent)

---

## 🎯 Quick Start Checklist

Before demo:
- [ ] Backend running: `cd backend && uvicorn main:app --reload --port 8000`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Verify in backend logs: `✅ MongoDB connected` and `✅ ChromaDB connected`
- [ ] Open browser to `http://localhost:3000`

---

## 🎬 Demo Flow (Recommended Order)

### Part 1: Live Pricing Demo (MongoDB)

**Show:** Real-time pricing with AI reasoning

1. **Select Phoenix** (default city)
2. **Select Sample Ride #001** (Sky Harbor → ASU)
3. **Click "Calculate Dynamic Price"**
4. **Point out:**
   - AI Reasoning bullets (numbered points)
   - "✅ Saved to database (RIDE-XXXXXX)" indicator
   - Surge multiplier and confidence score

5. **Click Play button** on AI Reasoning
   - Watch highlighting move through each point
   - Use Pause/Stop to control playback

6. **Change to Gold customer** → Recalculate
   - Show loyalty discount in reasoning

7. **Change city to New York** → Recalculate
   - Show SURGE demand thermometer
   - Higher prices due to demand

---

### Part 2: ChatBot Queries (MongoDB + ChromaDB RAG)

**Click the ChatBot icon (bottom right)**

#### MongoDB Queries (Real Data)

| Query | What it Shows |
|-------|---------------|
| "What's the average price?" | Real-time avg from 988 rides |
| "How many Gold customers?" | Customer count by loyalty tier |
| "Show me overall statistics" | Summary stats from database |

#### ChromaDB RAG Queries (Semantic Search) ⭐

| Query | What it Shows |
|-------|---------------|
| "Find Urban rides at Night" | RAG semantic search with similarity % |
| "Show Premium vehicle rides" | Vector similarity matching |
| "Find Rural Economy rides" | Cross-category semantic search |
| "What rides are similar to Morning Suburban?" | Pure semantic matching |

**Look for in response:** 
> "Using semantic search (RAG), I found X similar rides. Average price: $XXX (similarity: XX%)"

#### Weather Queries

| Query | What it Shows |
|-------|---------------|
| "What's the weather in Phoenix?" | Live weather data |
| "Current conditions in New York" | Real-time weather API |

---

## 📝 Full Query Library

### ✅ SAFE Queries (Use These!)

**Pricing & Rides:**
```
What's the average price?
What's the average ride price?
Find Urban rides at Night
Find Premium vehicle rides
Show Rural Economy rides
Find rides similar to Morning Urban
What's the typical surge multiplier?
Find Suburban rides in the Evening
```

**Customers:**
```
How many Gold customers?
How many Silver customers?
Show me customer breakdown
How many total customers?
```

**Statistics:**
```
Show me overall statistics
How many total rides?
What's the average duration?
How many active drivers?
```

**Weather:**
```
What's the weather in Phoenix?
Current weather in New York
Weather conditions in San Francisco
```

### ❌ AVOID These Queries

```
❌ "Say that again" (no conversation memory)
❌ "What about Gold?" (follow-up context)
❌ "Book me a ride" (we're analytics, not booking)
❌ "Average customer spend" (not implemented)
❌ Complex multi-part questions
```

---

## 🔥 Highlight Points for Judges

### 1. Hybrid Database Architecture
> "We use MongoDB for structured data and ChromaDB for semantic search - a true hybrid approach."

### 2. RAG in Action
> "Watch how ChromaDB finds semantically similar rides, not just exact matches."

### 3. Real-time Persistence
> "Every calculation is saved to MongoDB - the average price updates in real-time."

### 4. AI Transparency
> "The AI Reasoning shows exactly WHY this price was calculated - full explainability."

### 5. Voice Accessibility
> "Users can hear the reasoning read aloud with synchronized highlighting."

---

## 🛠️ Troubleshooting During Demo

| Issue | Quick Fix |
|-------|-----------|
| ChatBot says "I didn't find..." | Try different query wording |
| No ChromaDB results | Check backend logs for connection |
| Weather shows "couldn't fetch" | Use a supported city (Phoenix, New York, etc.) |
| Mic not working | Click mic to toggle, check browser permissions |
| Price seems wrong | It's using real historical data - explain this |

---

## 💬 Talking Points

**Opening:**
> "HoneyGo uses an AI agent powered by LangChain to make intelligent pricing decisions. Let me show you how it works..."

**During Calculate:**
> "Notice how the AI considers multiple factors - demand, weather, loyalty status - and explains its reasoning in plain English."

**During ChatBot:**
> "Our hybrid architecture uses ChromaDB for semantic search. Instead of exact keyword matching, it finds conceptually similar rides from our dataset of 988 historical records."

**Closing:**
> "This demonstrates how AI can make complex business decisions transparent and explainable - critical for enterprise adoption."

---

## 📊 Key Numbers to Remember

- **988** historical rides in dataset
- **500** customers (45 Gold, 120 Silver, 85 Bronze, 250 Regular)
- **5 cities** supported (Phoenix, New York, San Francisco, Chicago, Orlando)
- **4 time slots** (Morning, Afternoon, Evening, Night)
- **3 vehicle types** (Economy, Standard, Premium)
- **3 location types** (Urban, Suburban, Rural)

---

## 🎯 Demo Success Criteria

✅ Show real-time pricing calculation  
✅ Demonstrate AI reasoning transparency  
✅ Show ChromaDB semantic search (RAG)  
✅ Show MongoDB persistence ("Saved to database")  
✅ Voice playback with highlighting  
✅ Explain hybrid architecture  

---

**Good luck with the demo! 🍀**

