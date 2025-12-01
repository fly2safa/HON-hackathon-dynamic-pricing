# HoneyGo LangChain Agent

## Overview
ReAct (Reasoning + Acting) agent for intelligent dynamic pricing decisions with LangSmith observability.

## Key Features
- 🤖 **Multi-LLM Support** - OpenAI, Google AI, or Anthropic
- 🛡️ **Automatic Fallback** - Resilient to API failures
- 📊 **LangSmith Observability** - Real-time agent tracing
- 🔧 **Custom Tools** - Pricing calculator, database queries, weather data
- 💰 **Cost Optimized** - Falls back to cheaper providers if needed

## Structure
```
agent/
├── src/
│   ├── agent.py           # Main ReAct agent
│   ├── tools/             # Custom agent tools
│   │   ├── __init__.py
│   │   ├── pricing_calculator.py
│   │   ├── database_tool.py
│   │   └── weather_tool.py
│   └── config.py          # Configuration
├── tests/
│   └── test_agent.py
├── requirements.txt
└── README.md
```

## Setup
```bash
cd agent
pip install -r requirements.txt
```

## Environment Variables
The agent reads from the root `.env` file (shared across all services).

**Required (at least one):**
```bash
# Option 1: OpenAI (recommended)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key

# Option 2: Google AI (free/cheap)
LLM_PROVIDER=google
GOOGLE_API_KEY=your-key

# Option 3: Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-key
```

**Highly Recommended (FREE):**
```bash
LANGSMITH_API_KEY=lsv2_pt_your_key
LANGSMITH_PROJECT=honeygo-pricing
LANGSMITH_TRACING=true
```

**Automatic Fallback:**
The agent automatically tries providers in order:
1. Explicit `LLM_PROVIDER` (if set)
2. OpenAI (if key exists)
3. Google AI (if key exists)
4. Anthropic (if key exists)

This ensures the agent works even if one provider fails!

## Usage
See `src/agent.py` for implementation details.

