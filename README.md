# 🚖 HoneyGo: Intelligent Ride-Sharing Platform

> **Agentic AI-Powered Dynamic Pricing for Honeywell's Ride-Sharing Division**

[![Team](https://img.shields.io/badge/Team-%231-blue)]()
[![Hackathon](https://img.shields.io/badge/Hackathon-HON%20Dynamic%20Pricing-orange)]()
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()

---

## 📋 Project Overview

**HoneyGo** is an innovative Agentic AI solution for dynamic pricing in a ride-sharing context, demonstrating reasoning applicable to Honeywell's catalog demand pricing, supply constraints, and customer tier management.

### 🎯 Key Objectives

- **Maximize Profitability**: Intelligent pricing that balances demand, supply, and customer value
- **Agentic AI**: Autonomous reasoning with explainable decision-making using LangChain ReAct agents
- **Real-World Applicability**: Demonstrate concepts transferable to Honeywell's B2B catalog pricing
- **Explainability**: Full transparency into AI reasoning for trust and compliance

---

## 👥 Team #1

| Role | Name | Responsibilities |
|------|------|------------------|
| **Frontend + Voice Features** | Jason (Primary), Safa (Backup) | Next.js UI, Voice I/O |
| **MongoDB Engineer** | Jason | Database design, data import |
| **Backend/FastAPI Engineer** | Dari | API development, integration |
| **LangChain/Agent + LangSmith** | OPEN (Safa backup) | AI agent, observability |
| **ChromaDB/Vector DB Engineer** | OPEN (Safa backup) | RAG, semantic search |
| **n8n/MCP Workflow Engineer** | Steve | Workflow automation |
| **Project Lead/Coordinator** | OPEN (Safa natural fit) | Integration, coordination |
| **Presentation Slides** | Steve | Slide deck creation |
| **Live Demo Presenter** | Dari (Primary), Team (Support) | Demo execution |
| **Demo Video Creator** | OPEN | Backup video recording |
| **Docker/DevOps Engineer** | OPEN (Safa backup) | Containerization, deployment |

---

## 🛠️ Tech Stack

### **Frontend**
- **Next.js 14** (App Router)
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Recharts/Chart.js** for data visualization
- **Web Speech API** for voice features (Mic 🎤 & Speaker 🔊)

### **Backend**
- **FastAPI** (Python 3.11+)
- **Pydantic** for data validation
- **OpenAPI/Swagger** for API documentation

### **AI & Intelligence**
- **LangChain** (ReAct agent framework)
- **OpenAI GPT-4** or **Claude 3.5 Sonnet** (LLM)
- **LangSmith** (Agent observability & debugging)

### **Databases**
- **MongoDB Atlas** (Structured data: rides, customers, drivers, pricing)
- **ChromaDB** (Vector database for RAG & semantic search)

### **Workflow Automation**
- **n8n** or **MCP (Model Context Protocol)** (Workflow orchestration)

### **DevOps & Deployment**
- **Docker** & **Docker Compose** (Containerization)
- **Git/GitHub** (Version control, branching strategy)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and **npm**
- **Python** 3.11+
- **MongoDB Atlas** account (FREE M0 tier)
- **Docker** & **Docker Compose** (optional, for containerized deployment)
- **Git**

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fly2safa/HON-hackathon-dynamic-pricing.git
   cd HON-hackathon-dynamic-pricing
   ```

2. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys and connection strings
   ```

3. **Install dependencies**:
   ```bash
   # Frontend
   cd frontend
   npm install
   
   # Backend
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   # Frontend (from frontend/)
   npm run dev
   
   # Backend (from backend/)
   uvicorn main:app --reload
   ```

5. **Access the application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

### Docker Deployment (Optional)

```bash
# Build and run all services
docker-compose up --build

# Stop services
docker-compose down
```

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[Implementation Plan](docs/implementation-plan.md)** - Complete project roadmap, architecture, and team coordination
- **[MongoDB Design Decision](docs/mongoDB-design-decision.md)** - Multi-collection vs single collection rationale
- **[ChromaDB RAG Design](docs/chromadb-rag-design.md)** - Hybrid database approach and RAG benefits
- **[LangSmith Observability Proposal](docs/langsmith-observability-proposal.md)** - Agent tracing and explainability
- **[Project Structure Guide](docs/project-structure-guide.md)** - Folder structure, setup instructions, and sample code

---

## 🏗️ Project Structure

```
HON-hackathon-dynamic-pricing/
├── backend/              # FastAPI application
├── frontend/             # Next.js application
├── workflows/            # n8n/MCP configurations
├── data/                 # Data files and scripts
│   ├── raw/              # Original CSV/TSV files
│   ├── mongodb/          # MongoDB seed scripts
│   ├── chromadb/         # ChromaDB seed scripts
│   └── mock/             # Mock data for testing
├── docs/                 # Documentation
├── project-spec/         # Hackathon specifications
├── Dockerfile.backend    # Backend Docker configuration
├── Dockerfile.frontend   # Frontend Docker configuration
├── docker-compose.yml    # Multi-container orchestration
├── .dockerignore         # Docker ignore rules
├── env.example           # Environment variables template
└── README.md             # This file
```

---

## 🎯 Key Features

### 1. **Agentic AI with LangChain ReAct**
- Autonomous reasoning agent with 8+ custom tools
- Explainable decision-making with full reasoning traces
- LangSmith integration for observability and debugging

### 2. **Hybrid Database Architecture**
- **MongoDB**: Structured data (rides, customers, drivers, pricing decisions)
- **ChromaDB**: Vector database for RAG, semantic search, and contextual reasoning

### 3. **Dynamic Pricing Engine**
- Real-time pricing based on demand, supply, customer tier, and driver incentives
- Loyalty rewards and asset quality considerations
- Profitability optimization with explainability

### 4. **Voice-Enabled Interface** (Extra Features)
- 🎤 **Voice Input**: Speak queries to the AI bot
- 🔊 **Voice Output**: Hear AI responses read aloud

### 5. **Workflow Automation**
- n8n or MCP for orchestrating data pipelines and agent workflows

### 6. **Comprehensive Observability**
- LangSmith traces for every agent decision
- Real-time monitoring and debugging

---

## 📅 Timeline

| Date | Phase | Focus |
|------|-------|-------|
| **Nov 30** | Phase 1: Planning | Implementation plan, architecture design, team coordination |
| **Dec 1** | Phase 2: Foundation | API contracts, MongoDB setup, LangSmith setup, agent skeleton |
| **Dec 2** | Phase 3: Core Development | Backend integration, ChromaDB setup, agent tools, frontend components |
| **Dec 3** | Phase 4: Integration | Full-stack integration, RAG implementation, voice features |
| **Dec 4 AM** | Phase 5: Testing & Polish | Bug fixes, demo prep, Docker setup, final testing |
| **Dec 4 Midday** | Submission Deadline | GitHub repo + presentation slides submitted |
| **Dec 5** | Presentation Day | Live demo and Q&A |

---

## 🏆 Judging Criteria Alignment

| Criterion | Our Approach |
|-----------|--------------|
| **Innovation** | Agentic AI with RAG, hybrid database, voice features |
| **Technical Depth** | LangChain ReAct, MongoDB + ChromaDB, LangSmith observability |
| **Explainability** | Full reasoning traces, LangSmith dashboard, transparent pricing logic |
| **Applicability to HON** | 6 specific recommendations for Honeywell B2B pricing |
| **Presentation Quality** | Professional slides, live demo, backup video, key decision highlights |

---

## 📊 Deliverables

- ✅ **GitHub Repository**: Clean, well-documented codebase
- ✅ **Live Demo**: Functional application with AI agent reasoning
- ✅ **Presentation Slides**: 16-slide deck with key decisions highlighted
- ✅ **Demo Video**: Backup recording in case of technical issues
- ✅ **Documentation**: Comprehensive guides and architecture diagrams

---

## 🔗 Links

- **GitHub Repository**: [https://github.com/fly2safa/HON-hackathon-dynamic-pricing](https://github.com/fly2safa/HON-hackathon-dynamic-pricing)
- **LangSmith Dashboard**: (Team access provided via `.env`)
- **MongoDB Atlas**: (Connection string in `.env`)

---

## 📝 License

This project is developed for the HON Dynamic Pricing Hackathon (Team #1).

---

## 🙏 Acknowledgments

Special thanks to Honeywell and the hackathon organizers for this opportunity to explore Agentic AI in dynamic pricing!

---

**Built with ❤️ by Team #1 | Dec 2025**
