# HoneyGo LangChain Agent

## Overview
ReAct (Reasoning + Acting) agent for intelligent dynamic pricing decisions with LangSmith observability.

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
```
OPENAI_API_KEY=your_key
LANGSMITH_API_KEY=your_key
LANGSMITH_PROJECT=honeygo-pricing
```

## Usage
See `src/agent.py` for implementation details.

