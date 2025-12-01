"""
Configuration for HoneyGo LangChain Agent
Reads from root .env file (shared across all services)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (two levels up from this file)
root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / '.env'
load_dotenv(dotenv_path=env_path)

print(f"📁 Loading environment from: {env_path}")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai", "google", or "anthropic"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Validate that required API key is present
if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in .env")
elif LLM_PROVIDER == "google" and not GOOGLE_API_KEY:
    print("⚠️  WARNING: GOOGLE_API_KEY not found in .env")

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

