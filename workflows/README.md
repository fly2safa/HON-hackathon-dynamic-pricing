# Workflows - n8n Integration for HoneyGo

**Owner:** Role 6 (Steve - n8n/MCP Workflow Integration Engineer)  
**Status:** ✅ Implemented  
**Last Updated:** Dec 2, 2025

## Overview

External data enrichment workflows for HoneyGo dynamic pricing. These workflows fetch real-time weather, events, and traffic data to inform pricing decisions.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API   │────▶│   n8n Webhooks  │
│   (Next.js)     │     │   (FastAPI)     │     │   (localhost)   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                        ┌────────────────────────────────┼────────────────────────────────┐
                        │                                │                                │
                        ▼                                ▼                                ▼
               ┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
               │ Weather API     │             │ Events API      │             │ Traffic Calc    │
               │ (OpenWeather)   │             │ (Ticketmaster)  │             │ (Simulated)     │
               └─────────────────┘             └─────────────────┘             └─────────────────┘
```

## Quick Start

### 1. Start n8n
```bash
nvm use 24
n8n start
# Access UI at http://localhost:5678
```

### 2. Import Workflows
1. Open n8n UI → Click "Add Workflow"
2. Click ⋮ menu → "Import from File"
3. Import `workflows/n8n/pricing-enrichment-combined.json`

### 3. Activate Workflow
Toggle the workflow to "Active" to enable webhooks.

## Workflows

| Workflow | Webhook URL | Purpose |
|----------|-------------|---------|
| **pricing-enrichment-combined** ⭐ | `/webhook/pricing-enrichment` | All-in-one pricing factors |
| weather-enrichment | `/webhook/weather-data` | Weather conditions |
| event-fetcher | `/webhook/event-data` | Nearby events |
| traffic-data | `/webhook/traffic-data` | Traffic simulation |

## API Endpoints

The backend exposes these endpoints at `/n8n/`:

```
GET  /n8n/health              - Check n8n availability
GET  /n8n/weather/{city}      - Get weather data
GET  /n8n/events/{city}       - Get events data
GET  /n8n/traffic             - Get traffic data
POST /n8n/enrichment          - Combined pricing factors
GET  /n8n/demo/compare-cities - Compare two cities (for demo)
```

## Testing

```bash
# Test weather
curl http://localhost:8000/n8n/weather/Phoenix

# Test city comparison (Steve's demo idea)
curl "http://localhost:8000/n8n/demo/compare-cities?city1=Phoenix&city2=New%20York"
```

## Mock Data

For demo without API keys, use `data/mock/`:
- `mock_weather.json` - Weather scenarios
- `mock_events.json` - Event scenarios  
- `mock_traffic.json` - Traffic scenarios

## File Structure

```
workflows/
├── README.md
├── .env.workflows
└── n8n/
    ├── pricing-enrichment-combined.json  ⭐ Main workflow
    ├── weather-enrichment.json
    ├── event-fetcher.json
    └── traffic-data.json

backend/
├── services/n8n_service.py    # n8n webhook client
└── routers/n8n.py             # API endpoints
```

## Timeline
- [x] Dec 1: Set up n8n, create workflows
- [x] Dec 2: Backend integration
- [ ] Dec 3 PM: Test with full system
- [ ] Dec 4: Final testing
