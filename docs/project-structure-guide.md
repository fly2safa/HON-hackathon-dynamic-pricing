# HoneyGo Project Structure Guide

## Overview

This document explains the project folder structure and what each team member needs to create in their respective folders.

**Last Updated:** Nov 30, 2025  
**Status:** Ready for Dec 1 implementation

---

## Project Folder Structure

```
Hackathon/
├── backend/              # FastAPI application (Role 3: Dari)
├── frontend/             # Next.js application (Role 1: Jason)
├── workflows/            # n8n/MCP configurations (Role 6: Steve)
├── data/                 # Data files and seed scripts (Role 2: Jason, Role 5: Safa)
├── docs/                 # Documentation (already complete)
├── images/               # Project images (HoneyGo logo, etc.)
├── project-spec/         # Original hackathon specifications
├── .env.example          # Environment variables template
├── .env                  # Actual environment variables (gitignored)
├── .gitignore            # Git ignore rules
└── README.md             # Project overview
```

---

## Folder Details & Responsibilities

### 1. `backend/` - FastAPI Application

**Owner:** Role 3 (Dari - Backend/FastAPI Engineer)

**Purpose:** Python FastAPI backend that serves the API and integrates all components

**Folder Structure to Create:**
```
backend/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (copy from root .env)
├── routers/                   # API endpoint routers
│   ├── __init__.py
│   ├── pricing.py            # Pricing endpoints
│   ├── rides.py              # Ride data endpoints
│   └── health.py             # Health check endpoint
├── services/                  # Business logic
│   ├── __init__.py
│   ├── agent_service.py      # LangChain agent integration
│   ├── mongodb_service.py    # MongoDB queries
│   └── chromadb_service.py   # ChromaDB queries
├── models/                    # Pydantic data models
│   ├── __init__.py
│   ├── ride.py               # Ride model
│   ├── pricing.py            # Pricing request/response models
│   └── customer.py           # Customer model
└── utils/                     # Utility functions
    ├── __init__.py
    └── config.py             # Configuration management
```

**Key Files to Create (Dec 1):**

1. **`requirements.txt`** - Python dependencies:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pymongo==4.6.0
langchain==0.1.0
langchain-openai==0.0.2
chromadb==0.4.18
python-dotenv==1.0.0
httpx==0.25.2
```

2. **`main.py`** - FastAPI app skeleton:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="HoneyGo Dynamic Pricing API",
    description="Agentic AI for ride-sharing pricing",
    version="1.0.0"
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "HoneyGo API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routers here (after creating them)
# from routers import pricing, rides
# app.include_router(pricing.router)
# app.include_router(rides.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Timeline:**
- **Dec 1 AM:** Create folder structure and skeleton
- **Dec 1 PM:** Implement API endpoints
- **Dec 2:** Integrate MongoDB
- **Dec 3:** Integrate LangChain agent and ChromaDB
- **Dec 4:** Testing and polish

**Dependencies:**
- Needs MongoDB connection string from Jason (Role 2)
- Needs LangChain agent from Safa (Role 4)
- Needs ChromaDB connection from Safa (Role 5)

---

### 2. `frontend/` - Next.js Application

**Owner:** Role 1 (Jason - Frontend Developer)

**Purpose:** Next.js 14+ web application with modern UI for pricing interface

**Folder Structure to Create:**
```
frontend/
├── package.json               # Node dependencies
├── next.config.js             # Next.js configuration
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── .env.local                 # Environment variables
├── app/                       # Next.js 14+ app router
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   ├── pricing/              # Pricing page
│   │   └── page.tsx
│   └── globals.css           # Global styles
├── components/                # React components
│   ├── PricingForm.tsx       # Pricing input form
│   ├── PricingResult.tsx     # Pricing display
│   ├── ReasoningExplainer.tsx # Agent reasoning display
│   ├── VoiceInput.tsx        # Voice input (E1 - Extra)
│   └── VoiceOutput.tsx       # Voice output (E2 - Extra)
├── lib/                       # Utilities
│   ├── api.ts                # API client
│   └── types.ts              # TypeScript types
└── public/                    # Static assets
    └── logo.png              # HoneyGo logo
```

**Key Files to Create (Dec 1):**

1. **`package.json`** - Node dependencies:
```json
{
  "name": "honeygo-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    "@types/react": "18.2.45",
    "@types/node": "20.10.5",
    "tailwindcss": "3.3.6",
    "autoprefixer": "10.4.16",
    "postcss": "8.4.32",
    "axios": "1.6.2",
    "recharts": "2.10.3"
  }
}
```

2. **Initialize Next.js project:**
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
```

**Timeline:**
- **Dec 1 AM:** Set up Next.js project and folder structure
- **Dec 1 PM:** Build UI components with mock data
- **Dec 2:** Continue UI development
- **Dec 3 Eve:** Integrate with backend API
- **Dec 3-4:** Add voice features (E1, E2) if time permits
- **Dec 4:** Testing and polish

**Dependencies:**
- Needs API contract from Dari (Role 3) - Dec 1 AM
- Needs backend API running for integration - Dec 3 Eve

---

### 3. `workflows/` - n8n/MCP Configurations

**Owner:** Role 6 (Steve - n8n/MCP Workflow Integration Engineer)

**Purpose:** Workflow automation for external data integration

**Folder Structure to Create:**
```
workflows/
├── README.md                  # How to import/use workflows
├── n8n/                       # n8n workflows (if using n8n)
│   ├── weather-enrichment.json
│   ├── event-fetcher.json
│   └── traffic-data.json
├── mcp/                       # MCP configurations (if using MCP)
│   ├── mcp-config.yaml
│   └── tools/
│       ├── weather_tool.py
│       └── events_tool.py
└── .env.workflows             # Workflow-specific env vars
```

**Key Files to Create (Dec 1-2):**

1. **`README.md`** - Workflow documentation:
```markdown
# HoneyGo Workflows

## n8n Workflows (if using n8n)

### Setup
1. Install n8n: `npm install -g n8n`
2. Start n8n: `n8n start`
3. Import workflows from `n8n/` folder
4. Configure API credentials

### Workflows
- **weather-enrichment.json**: Fetches weather data and updates MongoDB
- **event-fetcher.json**: Fetches nearby events (concerts, sports)
- **traffic-data.json**: Fetches traffic conditions

## MCP Configuration (if using MCP)

### Setup
1. Install MCP dependencies
2. Configure `mcp-config.yaml`
3. Register tools with LangChain agent

### Tools
- **weather_tool.py**: Weather API integration
- **events_tool.py**: Events API integration
```

2. **External API Integrations:**
   - Weather API: OpenWeatherMap (FREE tier)
   - Events API: Ticketmaster or mock data
   - Traffic API: Google Maps or mock data

**Timeline:**
- **Dec 1:** Set up n8n or MCP environment
- **Dec 2:** Create workflows for external data
- **Dec 3 PM:** Integrate with backend (coordinate with Dari)
- **Dec 4:** Testing

**Dependencies:**
- Needs backend API endpoints from Dari (Role 3) - Dec 3 PM

**Decision:** Steve will choose n8n OR MCP based on familiarity

---

### 4. `data/` - Data Files & Seed Scripts

**Owners:** 
- Role 2 (Jason - MongoDB seed scripts)
- Role 5 (Safa - ChromaDB seed scripts)

**Purpose:** Centralized location for all data files and database seeding scripts

**Folder Structure to Create:**
```
data/
├── README.md                  # Data documentation
├── raw/                       # Original data files
│   ├── dynamic_pricing.csv   # Original dataset (1000 records)
│   └── dynamic_pricing.tsv   # Alternative format
├── mongodb/                   # MongoDB seed scripts
│   ├── seed_mongodb.py       # Main seeding script
│   ├── rides_data.json       # Processed ride data
│   ├── customers_data.json   # Customer profiles
│   └── drivers_data.json     # Driver profiles
├── chromadb/                  # ChromaDB seed scripts
│   ├── seed_chromadb.py      # Main seeding script
│   ├── hon_knowledge.json    # HON domain knowledge (20+ items)
│   └── pricing_reasoning.json # Historical pricing reasoning
└── mock/                      # Mock data for development
    ├── mock_weather.json     # Sample weather data
    ├── mock_events.json      # Sample events data
    └── mock_api_responses.json # Sample API responses
```

**Key Files to Create:**

1. **MongoDB Seed Script (`mongodb/seed_mongodb.py`)** - Jason creates:
```python
import pymongo
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = client["honeygo"]

def seed_rides():
    """Seed rides collection from CSV"""
    df = pd.read_csv("../raw/dynamic_pricing.csv")
    rides = df.to_dict('records')
    
    # Add timestamps
    for ride in rides:
        ride['created_at'] = datetime.now()
    
    db.rides.insert_many(rides)
    print(f"Inserted {len(rides)} rides")

def seed_customers():
    """Seed customers collection"""
    # Create customer profiles from rides data
    customers = [
        {
            "customer_id": f"CUST_{i:04d}",
            "loyalty_status": "Gold" if i % 3 == 0 else "Silver",
            "total_rides": i * 10,
            "created_at": datetime.now()
        }
        for i in range(1, 101)
    ]
    
    db.customers.insert_many(customers)
    print(f"Inserted {len(customers)} customers")

def seed_drivers():
    """Seed drivers collection"""
    drivers = [
        {
            "driver_id": f"DRV_{i:04d}",
            "name": f"Driver {i}",
            "rating": 4.5 + (i % 5) * 0.1,
            "total_earnings": i * 1000,
            "total_rides": i * 50,
            "created_at": datetime.now()
        }
        for i in range(1, 51)
    ]
    
    db.drivers.insert_many(drivers)
    print(f"Inserted {len(drivers)} drivers")

if __name__ == "__main__":
    print("Seeding MongoDB...")
    seed_rides()
    seed_customers()
    seed_drivers()
    print("MongoDB seeding complete!")
```

2. **ChromaDB Seed Script (`chromadb/seed_chromadb.py`)** - Safa creates:
```python
import chromadb
from chromadb.config import Settings
import json
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chromadb_data"
))

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def seed_hon_knowledge():
    """Seed HON knowledge base"""
    collection = client.create_collection("hon_knowledge")
    
    knowledge = [
        {
            "id": "HON_001",
            "text": "Honeywell aerospace parts pricing considers supply chain constraints and customer contract tiers",
            "category": "pricing_strategy"
        },
        {
            "id": "HON_002",
            "text": "Dynamic demand pricing must balance profitability with customer retention",
            "category": "business_rule"
        },
        # Add 18+ more items
    ]
    
    for item in knowledge:
        embedding = model.encode(item["text"]).tolist()
        collection.add(
            ids=[item["id"]],
            embeddings=[embedding],
            documents=[item["text"]],
            metadatas=[{"category": item["category"]}]
        )
    
    print(f"Inserted {len(knowledge)} HON knowledge items")

def seed_pricing_reasoning():
    """Seed historical pricing reasoning"""
    collection = client.create_collection("pricing_reasoning")
    
    # Add historical pricing decisions with reasoning
    # (Safa will populate this)
    
    print("Pricing reasoning collection created")

if __name__ == "__main__":
    print("Seeding ChromaDB...")
    seed_hon_knowledge()
    seed_pricing_reasoning()
    print("ChromaDB seeding complete!")
```

3. **HON Knowledge Base (`chromadb/hon_knowledge.json`)** - Safa creates:
```json
[
  {
    "id": "HON_001",
    "text": "Honeywell aerospace parts pricing considers supply chain constraints and customer contract tiers",
    "category": "pricing_strategy"
  },
  {
    "id": "HON_002",
    "text": "Dynamic demand pricing must balance profitability with customer retention",
    "category": "business_rule"
  },
  {
    "id": "HON_003",
    "text": "High-value customers receive priority pricing and inventory allocation",
    "category": "customer_tier"
  }
  // Add 17+ more items (total 20+)
]
```

**Timeline:**
- **Dec 1:** Move CSV files to `data/raw/`
- **Dec 1-2:** Jason creates MongoDB seed scripts
- **Dec 1-2:** Safa creates ChromaDB seed scripts and HON knowledge
- **Dec 2:** Run seeding scripts to populate databases

**Dependencies:**
- Needs MongoDB Atlas connection string (Jason sets up)
- Needs ChromaDB setup (Safa sets up)

---

### 5. `docs/` - Documentation (Already Complete)

**Status:** ✅ Complete

**Contents:**
- `implementation-plan.md` - Comprehensive project plan (150+ pages)
- `mongoDB-design-decision.md` - MongoDB schema justification
- `chromadb-rag-design.md` - ChromaDB RAG design
- `langsmith-observability-proposal.md` - LangSmith integration
- `potential-company-names.md` - Company naming options
- `project-structure-guide.md` - This document

**No action needed** - Documentation is ready for team reference

---

### 6. `images/` - Project Images (Already Complete)

**Status:** ✅ Complete

**Contents:**
- `honeygo-logo.png` - Company logo

**No action needed** - Logo ready for use in frontend and slides

---

### 7. `project-spec/` - Hackathon Specifications (Already Complete)

**Status:** ✅ Complete

**Contents:**
- Original hackathon documents and dataset
- Reference only, do not modify

**No action needed** - Keep for reference

---

## Environment Variables Setup

### `.env.example` (Template - Already Created)

**Location:** Root directory

**Contents:**
```bash
# ============================================
# LangSmith (Agent Observability)
# ============================================
# LANGSMITH_API_KEY is primary; LANGCHAIN_API_KEY also works
LANGSMITH_API_KEY=lsv2_pt_your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=honeygo-pricing

# ============================================
# LLM Provider (REQUIRED - Choose One)
# ============================================
OPENAI_API_KEY=sk-your_openai_key
# OR
# ANTHROPIC_API_KEY=sk-ant-your_anthropic_key

# ============================================
# MongoDB Atlas (Cloud Database)
# ============================================
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/honeygo?retryWrites=true&w=majority

# ============================================
# ChromaDB (Local Vector Database)
# ============================================
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_PERSIST_DIRECTORY=./chromadb_data

# ============================================
# Backend API
# ============================================
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# ============================================
# External APIs (Optional for Demo)
# ============================================
# WEATHER_API_KEY=your_weather_key
# EVENTS_API_KEY=your_events_key
# TRAFFIC_API_KEY=your_traffic_key
```

### `.env` (Actual - Create from .env.example)

**Setup Instructions:**

1. **Copy template:**
```bash
cp .env.example .env
```

2. **Update with real values:**
   - **LangSmith API Key:** Safa creates account and shares key (Dec 1)
   - **OpenAI API Key:** Team decides who provides (Dec 1)
   - **MongoDB URI:** Jason creates Atlas cluster and shares (Dec 1)
   - **ChromaDB:** Safa sets up locally (Dec 1-2)

3. **Share with team:**
   - Post keys in Slack (secure channel)
   - Everyone copies to their local `.env`
   - **NEVER commit `.env` to Git** (already in `.gitignore`)

---

## Quick Start Guide for Each Role

### Role 1 (Jason - Frontend + MongoDB)

**Day 1 Tasks:**
1. Set up MongoDB Atlas cluster (FREE M0 tier)
2. Share connection string with team
3. Create `data/mongodb/` seed scripts
4. Initialize Next.js project in `frontend/`
5. Build UI components with mock data

**Commands:**
```bash
# MongoDB seeding
cd data/mongodb
python seed_mongodb.py

# Frontend setup
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

---

### Role 2 (Dari - Backend)

**Day 1 Tasks:**
1. Wait for API contract agreement with Jason (3 AM)
2. Create `backend/` folder structure
3. Set up FastAPI skeleton
4. Define API endpoints

**Commands:**
```bash
cd backend
pip install -r requirements.txt
python main.py  # Runs on http://localhost:8000
# Or: uvicorn main:app --reload
```

---

### Role 3 (Safa - LangChain + ChromaDB)

**Day 1 Tasks:**
1. Set up LangSmith account and share API key
2. Build LangChain agent with mock tools
3. Set up ChromaDB locally
4. Create `data/chromadb/` seed scripts
5. Seed HON knowledge base

**Commands:**
```bash
# Install dependencies
pip install langchain langchain-openai chromadb sentence-transformers

# Seed ChromaDB
cd data/chromadb
python seed_chromadb.py

# Test agent locally
python test_agent.py
```

---

### Role 4 (Steve - n8n/MCP + Slides)

**Day 1 Tasks:**
1. Choose n8n or MCP approach
2. Set up workflow environment
3. Create `workflows/` folder structure
4. Start presentation slide deck

**Commands (if using n8n):**
```bash
# Install n8n
npm install -g n8n

# Start n8n
n8n start  # Runs on http://localhost:5678

# Import workflows from workflows/n8n/
```

---

## File Creation Checklist

### ✅ Already Created (No Action Needed)
- [x] `docs/` - All documentation complete
- [x] `images/` - HoneyGo logo
- [x] `project-spec/` - Hackathon specifications
- [x] `.gitignore` - Git ignore rules
- [x] `README.md` - Project overview
- [x] `.env.example` - Environment variables template

### 📋 To Be Created (Dec 1)
- [ ] `backend/` folder structure (Dari)
- [ ] `frontend/` folder structure (Jason)
- [ ] `workflows/` folder structure (Steve)
- [ ] `data/mongodb/` seed scripts (Jason)
- [ ] `data/chromadb/` seed scripts (Safa)
- [ ] `.env` file (Everyone copies from `.env.example`)

---

## Common Commands Reference

### Backend (FastAPI)
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
# Or: uvicorn main:app --reload

# Access API docs
# http://localhost:8000/docs (Swagger UI)
```

### Frontend (Next.js)
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Access frontend
# http://localhost:3000
```

### Database Seeding
```bash
# MongoDB
cd data/mongodb
python seed_mongodb.py

# ChromaDB
cd data/chromadb
python seed_chromadb.py
```

### n8n (if using)
```bash
# Install
npm install -g n8n

# Start
n8n start

# Access UI
# http://localhost:5678
```

---

## 7. Docker Setup (Optional but Recommended)

**Owner:** Role 11 (OPEN - Safa can do if no one else is interested)

**Purpose:** Containerize the application for easy deployment and consistent environments

### Files to Create:

#### `Dockerfile.backend`
```dockerfile
# Backend Dockerfile for FastAPI
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### `Dockerfile.frontend`
```dockerfile
# Frontend Dockerfile for Next.js
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy application code
COPY frontend/ .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
```

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
      - LANGCHAIN_PROJECT=${LANGCHAIN_PROJECT}
      - LANGCHAIN_TRACING_V2=${LANGCHAIN_TRACING_V2}
    depends_on:
      - chromadb
    networks:
      - honeygo-network

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    networks:
      - honeygo-network

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chromadb-data:/chroma/chroma
    networks:
      - honeygo-network

networks:
  honeygo-network:
    driver: bridge

volumes:
  chromadb-data:
```

#### `.dockerignore`
```
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Environment
.env
.env.local

# Git
.git/
.gitignore

# Documentation
docs/
project-spec/
*.md

# Build outputs
.next/
dist/
build/

# Logs
*.log
npm-debug.log*
```

### Docker Commands:

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild a specific service
docker-compose build backend
docker-compose up backend
```

### Timeline:
- **Dec 2 Afternoon**: Create Dockerfiles and basic docker-compose.yml
- **Dec 3 Afternoon**: Add MongoDB and ChromaDB to docker-compose, test full deployment
- **Dec 4 Morning**: Finalize and document Docker setup

### Benefits:
- ✅ One-command deployment for judges/reviewers
- ✅ Consistent environment across team members
- ✅ Production-ready containerization
- ✅ Easy to demonstrate DevOps best practices

---

## Troubleshooting

### "Module not found" errors
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### "Connection refused" errors
- Check if MongoDB Atlas is accessible
- Verify `.env` has correct connection strings
- Ensure services are running (backend, frontend)

### "API key invalid" errors
- Verify `.env` has correct API keys
- Check LangSmith/OpenAI keys are active
- Ensure `.env` is loaded (use `python-dotenv`)

---

## Questions?

**Slack Channels:**
- `#general` - General questions
- `#blockers` - Immediate help needed
- `#integration` - Coordination questions

**Reference Documents:**
- `docs/implementation-plan.md` - Full project plan
- `docs/mongoDB-design-decision.md` - Database design
- `docs/chromadb-rag-design.md` - RAG design
- `docs/langsmith-observability-proposal.md` - LangSmith setup

---

**Last Updated:** Nov 30, 2025  
**Ready for:** Dec 1, 12:01 AM implementation start! 🚀

