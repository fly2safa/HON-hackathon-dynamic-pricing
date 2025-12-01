"""
Configuration for HoneyGo LangChain Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "google"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model selection based on provider
if LLM_PROVIDER == "google":
    AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-pro")
else:
    AGENT_MODEL = os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")

AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
AGENT_MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", "10"))

# LangSmith Configuration
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "honeygo-pricing")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true").lower() == "true"

# Database Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/honeygo_pricing")
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))

# Agent Behavior
VERBOSE = True  # Show agent reasoning in console

