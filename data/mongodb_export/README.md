# MongoDB Export Data

This directory contains exported data from the cloud MongoDB database for local development.

## 📦 Contents

| File | Documents | Size | Description |
|------|-----------|------|-------------|
| `customers.json` | 988 | ~497 KB | Customer profiles and loyalty data |
| `rides.json` | 1,000 | ~642 KB | Ride requests and history |
| `pricing_decisions.json` | 1,000 | ~2.6 MB | Historical pricing decisions from AI agent |
| `drivers.json` | 159 | ~140 KB | Driver information |
| `external_data.json` | 1,200 | ~753 KB | Weather, events, and traffic data |
| `metadata.json` | N/A | <1 KB | Export metadata and statistics |

**Total:** 4,347 documents (~4.6 MB)

## 🔄 Usage

### Import to Local MongoDB

```bash
# From project root
python import_mongodb_data.py
```

This will create a local MongoDB database named `HoneyGo` with all the collections.

### Re-export Fresh Data

```bash
# From project root
python export_mongodb_data.py
```

This will overwrite the JSON files with the latest data from the cloud database.

## 📝 Notes

- **Version Control:** These JSON files ARE committed to Git for team sharing
- **Size:** Total ~4.6 MB (acceptable for Git)
- **Format:** Standard JSON with pretty printing (indent=2)
- **MongoDB _id:** Excluded from export (will be auto-generated on import)
- **Data Types:** Dates are converted to ISO 8601 strings

## 🔐 Security

⚠️ **Important:** This data is for development purposes only. It contains mock/sample data.

- Do NOT commit real customer data
- Do NOT commit sensitive information
- Review data before committing to Git

## 🗓️ Last Updated

Check `metadata.json` for the latest export date and statistics.

```bash
cat metadata.json
```

