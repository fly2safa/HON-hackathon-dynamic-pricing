# Backend - FastAPI Application

**Owner:** Role 3 (Dari - Backend/FastAPI Engineer)

## Purpose
Python FastAPI backend that serves the API and integrates all components (MongoDB, LangChain agent, ChromaDB, n8n/MCP).

## Setup Instructions

### 1. Create Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` from root to `.env` and update with real values.

### 4. Run Development Server
```bash
python main.py
# Or: uvicorn main:app --reload
```

Server runs on: http://localhost:8000

API Documentation: http://localhost:8000/docs (Swagger UI)

## Folder Structure to Create

```
backend/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
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

## Timeline
- **Dec 1 AM:** Create folder structure and skeleton
- **Dec 1 PM:** Implement API endpoints
- **Dec 2:** Integrate MongoDB
- **Dec 3:** Integrate LangChain agent and ChromaDB
- **Dec 4:** Testing and polish

## Dependencies
- MongoDB connection string from Jason (Role 2)
- LangChain agent from Safa (Role 4)
- ChromaDB connection from Safa (Role 5)

## Reference
See `docs/project-structure-guide.md` for detailed setup instructions and sample code.

