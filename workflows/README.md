# Workflows - n8n/MCP Configurations

**Owner:** Role 6 (Steve - n8n/MCP Workflow Integration Engineer)

## Purpose
Workflow automation for external data integration (weather, events, traffic).

## Decision: n8n OR MCP

Steve will choose one approach based on familiarity:

### Option 1: n8n (Visual Workflow Builder)
- Visual workflow editor
- Easy to configure and test
- Export workflows as JSON

### Option 2: MCP (Model Context Protocol)
- More programmatic approach
- Better LangChain integration
- Python-based tools

## Setup Instructions

### If Using n8n:

1. **Install n8n:**
```bash
npm install -g n8n
```

2. **Start n8n:**
```bash
n8n start
```

Access UI: http://localhost:5678

3. **Create Workflows:**
   - Weather enrichment
   - Event fetcher
   - Traffic data

4. **Export Workflows:**
   - Save as JSON in `workflows/n8n/`

### If Using MCP:

1. **Install MCP dependencies:**
```bash
pip install mcp langchain
```

2. **Create Tools:**
   - `tools/weather_tool.py`
   - `tools/events_tool.py`
   - `tools/traffic_tool.py`

3. **Configure:**
   - Create `mcp-config.yaml`
   - Register tools with LangChain agent

## Folder Structure

```
workflows/
├── README.md                  # This file
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

## External APIs

### Weather API (Recommended: OpenWeatherMap)
- FREE tier: 1,000 calls/day
- Sign up: https://openweathermap.org/api
- Add key to `.env`: `WEATHER_API_KEY=your_key`

### Events API (Options)
- Ticketmaster API (FREE tier)
- Or use mock data: `data/mock/mock_events.json`

### Traffic API (Options)
- Google Maps API (requires billing)
- Or use mock data: `data/mock/mock_traffic.json`

## Timeline
- **Dec 1:** Set up n8n or MCP environment
- **Dec 2:** Create workflows for external data
- **Dec 3 PM:** Integrate with backend (coordinate with Dari)
- **Dec 4:** Testing

## Dependencies
- Backend API endpoints from Dari (Role 3) - Dec 3 PM

## Reference
See `docs/project-structure-guide.md` for detailed setup instructions.

