# HoneyGo Testing Tracker

A GUI-based manual testing tool for the HoneyGo Dynamic Pricing application.

## Features

- 📋 **40+ Test Cases** organized by category
- 💡 **Hints** for each test to guide execution
- 📊 **Progress Tracking** with pass/fail statistics
- 💾 **Save/Load** test progress as JSON
- 📝 **Generate Reports** as Markdown
- 🔗 **Quick Links** to Frontend, API Docs, LangSmith

## Quick Start

### Prerequisites
- Python 3.8+ with tkinter (usually included)
- HoneyGo backend running on port 8000
- HoneyGo frontend running on port 3000

### 1. Navigate to Testing Tool

**Windows (PowerShell/CMD):**
```powershell
cd testing_tool
```

**macOS/Linux (bash):**
```bash
cd testing_tool
```

### 2. Install Requirements (if needed)

**Windows (PowerShell):**
```powershell
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

> Note: This tool uses Python's built-in `tkinter` library. If tkinter is missing:
> - **Windows:** Usually included with Python installer
> - **macOS:** `brew install python-tk@3.11` (adjust version)
> - **Linux (Ubuntu/Debian):** `sudo apt-get install python3-tk`
> - **Linux (Fedora):** `sudo dnf install python3-tkinter`

### 3. Run the Testing Tracker

**Windows (PowerShell/CMD):**
```powershell
python honeygo_test_tracker.py
```

**macOS/Linux:**
```bash
python3 honeygo_test_tracker.py
```

### 4. Enter Your Name
When prompted, enter your name for tracking purposes.

### 5. Start Testing
- Click on test cases in the left panel
- Read the steps and hints
- Execute the test manually
- Set status: Pass, Fail, or Blocked
- Add notes if needed
- Click "Save" periodically

## Test Categories

| Section | Tests | Description |
|---------|-------|-------------|
| Backend | 4 | Server startup, health checks, API docs |
| Frontend | 3 | UI loading, backend connection |
| LangSmith | 3 | Observability integration |
| Weather | 3 | Real weather data, AI reasoning |
| Demand | 3 | Surge pricing, thermometer sync |
| Loyalty | 4 | Tier discounts, competitor pricing |
| Cities | 4 | Multi-city pricing, Waymo |
| UI | 4 | Animations, formatting |
| Mock/Real | 3 | Backend fallback behavior |
| Scheduling | 2 | Future ride booking |
| E2E | 3 | End-to-end scenarios |

## Saving Results

Results are saved to `testing_tool/results/`:
- `test_progress_<name>_<timestamp>.json` - Raw data
- `test_report_<name>_<timestamp>.md` - Markdown report

## Quick Links (in Footer)

- 🏠 **Open Frontend** - http://localhost:3000
- 📖 **Open Docs** - http://localhost:8000/docs  
- 🌐 **Open LangSmith** - https://smith.langchain.com/

## Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│  🍯 HoneyGo Testing Tracker          Progress: 5/40 (12%)  │
├─────────────────────────────────────────────────────────────┤
│ [Backend] [Frontend] [LangSmith] [Weather] [Demand] ...    │
├───────────────────┬─────────────────────────────────────────┤
│ ▼ Backend         │ Test Case Details                       │
│   ✅ 1.1 Server   │ ─────────────────                       │
│   ✅ 1.2 Health   │ Title: 1.3 API Documentation            │
│   ⬜ 1.3 API Docs │ Description: Verify Swagger UI...       │
│   ⬜ 1.4 MongoDB  │                                         │
│ ▼ Frontend        │ Test Steps:                             │
│   ⬜ 2.1 Start    │ 1. Open http://localhost:8000/docs      │
│   ...             │ 2. Verify Swagger UI loads...           │
│                   │                                         │
│                   │ 💡 Hints:                               │
│                   │ ReDoc also available at /redoc          │
│                   │                                         │
│                   │ Status: ⬜ Not Started                  │
│                   │                                         │
│                   │ Notes:                                  │
│                   │ ┌─────────────────────────────────────┐ │
│                   │ │                                     │ │
│                   │ └─────────────────────────────────────┘ │
├───────────────────┴─────────────────────────────────────────┤
│ [⬅ Previous] [Next ➡]           [Frontend] [Docs] [Smith]  │
└─────────────────────────────────────────────────────────────┘
```

## Tips for Testers

1. **Start the servers first** - Backend (port 8000) and Frontend (port 3000)
2. **Test in order** - Backend → Frontend → Features
3. **Use the hints** - They provide useful context
4. **Add notes** - Document any issues or observations
5. **Save often** - Don't lose your progress!
6. **Generate report** - Share with the team when done

