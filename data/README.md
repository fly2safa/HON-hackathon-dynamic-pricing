# Data - Data Files & Seed Scripts

**Owners:** 
- Role 2 (Jason - MongoDB seed scripts)
- Role 5 (Safa - ChromaDB seed scripts)

## Purpose
Centralized location for all data files and database seeding scripts.

## Folder Structure

```
data/
├── README.md                  # This file
├── raw/                       # Original data files
│   ├── dynamic_pricing.csv   # Original dataset (1000 records)
│   └── dynamic_pricing.tsv   # Alternative format
├── mongodb_export/            # MongoDB exported data (for local dev) ✨ NEW
│   ├── customers.json        # 988 customer documents (497 KB)
│   ├── rides.json            # 1000 ride documents (642 KB)
│   ├── pricing_decisions.json # 1000 pricing decisions (2.6 MB)
│   ├── drivers.json          # 159 driver documents (140 KB)
│   ├── external_data.json    # 1200 external data documents (753 KB)
│   ├── metadata.json         # Export metadata
│   └── README.md             # Export documentation
├── mongodb/                   # MongoDB seed scripts (Jason) - git ignored
│   ├── seed_mongodb.py       # Main seeding script
│   ├── rides_data.json       # Processed ride data
│   ├── customers_data.json   # Customer profiles
│   └── drivers_data.json     # Driver profiles
├── chromadb/                  # ChromaDB data files - git ignored
│   ├── seed_chromadb.py      # Main seeding script
│   ├── hon_knowledge.json    # HON domain knowledge (20+ items)
│   └── pricing_reasoning.json # Historical pricing reasoning
└── mock/                      # Mock data for development
    ├── mock_weather.json     # Sample weather data
    ├── mock_events.json      # Sample events data
    └── mock_api_responses.json # Sample API responses
```

## MongoDB Seeding (Jason - Role 2)

### 1. Move CSV to raw/ folder
```bash
# Copy from project-spec to data/raw
cp ../project-spec/dynamic_pricing*.csv raw/
```

### 2. Create seed script
Create `mongodb/seed_mongodb.py` (see `docs/project-structure-guide.md` for sample code)

### 3. Run seeding
```bash
cd mongodb
python seed_mongodb.py
```

### Collections to Create:
- `rides` - 1000+ records from CSV
- `customers` - 100+ customer profiles
- `drivers` - 50+ driver profiles
- `pricing_decisions` - Empty (populated by agent)
- `external_data` - Empty (populated by n8n/MCP)

## ChromaDB Seeding (Safa - Role 5)

### 1. Create HON knowledge base
Create `chromadb/hon_knowledge.json` with 20+ items (see `docs/project-structure-guide.md` for sample)

**Note:** This is created knowledge based on public information about Honeywell's business and general aerospace industry principles.

### 2. Create seed script
Create `chromadb/seed_chromadb.py` (see `docs/project-structure-guide.md` for sample code)

### 3. Run seeding
```bash
cd chromadb
python seed_chromadb.py
```

### Collections to Create:
- `hon_knowledge` - 20+ HON domain knowledge items
- `pricing_reasoning` - Historical pricing decisions with reasoning
- `similar_contexts` - Semantically similar pricing scenarios

## Mock Data (Optional)

For development and testing without external APIs:

### `mock/mock_weather.json`
```json
{
  "location": "Phoenix, AZ",
  "temperature": 75,
  "condition": "Clear",
  "timestamp": "2025-12-01T18:00:00Z"
}
```

### `mock/mock_events.json`
```json
[
  {
    "name": "Suns Game",
    "venue": "Footprint Center",
    "time": "2025-12-01T19:00:00Z",
    "attendance": 18000
  }
]
```

## Timeline

### Dec 1:
- [ ] Jason: Move CSV files to `raw/`
- [ ] Jason: Create MongoDB seed scripts
- [ ] Safa: Create HON knowledge base JSON

### Dec 2:
- [ ] Jason: Run MongoDB seeding
- [ ] Safa: Create ChromaDB seed scripts
- [ ] Safa: Run ChromaDB seeding

## Dependencies
- MongoDB Atlas connection string (Jason sets up Dec 1)
- ChromaDB setup (Safa sets up Dec 1)

## 🆕 Local MongoDB Setup (Dec 2, 2025)

### Quick Start - Run MongoDB Locally

**Why?** Faster development, offline access, full read/write permissions.

**Steps:**
1. **Export cloud data** (already done - see `mongodb_export/`)
2. **Install MongoDB locally** (see `MONGODB_LOCAL_SETUP.md` in project root)
3. **Import data:**
   ```bash
   cd /home/jason/Python/AzNext_VibeCoding/HON-hackathon-dynamic-pricing
   python import_mongodb_data.py
   ```
4. **Update `.env`:**
   ```bash
   # Switch from cloud to local
   MONGODB_URI=mongodb://localhost:27017/HoneyGo
   ```

**Exported Data:**
- ✅ `mongodb_export/` - Contains 4,347 documents (~4.6 MB)
- ✅ Committed to Git for team sharing
- ✅ Use `export_mongodb_data.py` to refresh from cloud
- ✅ Use `import_mongodb_data.py` to import to local MongoDB

See `MONGODB_LOCAL_SETUP.md` for complete instructions.

## Reference
See `docs/project-structure-guide.md` for detailed instructions and sample code.

