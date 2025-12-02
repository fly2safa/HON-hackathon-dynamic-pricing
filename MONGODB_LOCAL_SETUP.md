# MongoDB Local Setup Guide

This guide will help you set up a local MongoDB instance on your laptop and copy the cloud database data to it.

---

## 📋 Overview

**Why run MongoDB locally?**
- ✅ Faster development (no network latency)
- ✅ Work offline
- ✅ Test without affecting cloud data
- ✅ No cloud database costs during development

---

## 🛠️ Step 1: Install MongoDB Locally

### Option A: Using Docker (Recommended - Easiest)

```bash
# Pull and run MongoDB in Docker
docker run -d \
  --name mongodb-local \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# Verify it's running
docker ps | grep mongodb-local
```

**To stop/start later:**
```bash
docker stop mongodb-local
docker start mongodb-local
```

### Option B: Install MongoDB Directly on Linux (Ubuntu/Debian)

```bash
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod  # Auto-start on boot

# Check status
sudo systemctl status mongod
```

### Option C: Install on macOS

```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Check status
brew services list
```

### Option D: Install on Windows

1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Run the installer (use default settings)
3. MongoDB will start automatically as a Windows Service

---

## 📦 Step 2: Export Data from Cloud Database

Export all data from the cloud MongoDB to JSON files:

```bash
cd /home/jason/Python/AzNext_VibeCoding/HON-hackathon-dynamic-pricing

# Activate virtual environment
source venv/bin/activate

# Export data (requires MONGODB_URI in .env pointing to cloud)
python export_mongodb_data.py
```

**Expected output:**
```
📦 Exporting MongoDB Data
✅ Connected to cloud database
✅ customers: 988 documents → customers.json
✅ rides: 1000 documents → rides.json
✅ pricing_decisions: 1000 documents → pricing_decisions.json
✅ drivers: 159 documents → drivers.json
✅ external_data: 1200 documents → external_data.json

📊 Export Summary:
  Collections exported: 5
  Total documents: 4347
  Export location: data/mongodb_export
```

**Files created:**
- `data/mongodb_export/customers.json`
- `data/mongodb_export/rides.json`
- `data/mongodb_export/pricing_decisions.json`
- `data/mongodb_export/drivers.json`
- `data/mongodb_export/external_data.json`
- `data/mongodb_export/metadata.json`

---

## 📥 Step 3: Import Data to Local MongoDB

Import the exported JSON files into your local MongoDB:

```bash
# Import to local MongoDB (default: localhost:27017/HoneyGo)
python import_mongodb_data.py

# Or specify custom URI and database name
python import_mongodb_data.py --uri mongodb://localhost:27017/ --db HoneyGo
```

**Expected output:**
```
📥 Importing MongoDB Data to Local Database
✅ Connected to local MongoDB
✅ customers: 988 documents imported
✅ rides: 1000 documents imported
✅ pricing_decisions: 1000 documents imported
✅ drivers: 159 documents imported
✅ external_data: 1200 documents imported

📊 Import Summary:
  Collections imported: 5
  Total documents: 4347
```

---

## ⚙️ Step 4: Update .env File

### Current .env (Cloud Database):
```bash
MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority
```

### Option 1: Switch to Local Database

**Replace the line in `.env` with:**
```bash
# Local MongoDB (read/write access)
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

### Option 2: Keep Both (Recommended)

**Add both to `.env` and comment out the one you're not using:**

```bash
# Cloud MongoDB (read-only)
# MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority

# Local MongoDB (read/write access) - ACTIVE
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

**To switch back to cloud:** Just swap which line is commented out!

---

## ✅ Step 5: Verify Local Setup

Test that your application can connect to the local database:

```bash
# Test connection
python test_mongodb_connection.py
```

**Expected output:**
```
✅ Successfully connected to MongoDB!
📚 Database: HoneyGo
📊 Found 5 collection(s):
  ✅ customers: 988 documents
  ✅ rides: 1000 documents
  ✅ pricing_decisions: 1000 documents
  ✅ drivers: 159 documents
  ✅ external_data: 1200 documents
```

**Test read/write access (local has full access):**
```bash
# This will show you can now write to the database
# (Unlike the read-only cloud database)
python test_mongodb_readonly.py
```

---

## 🔄 Syncing Data

### Re-export from Cloud (Get Latest Data)

```bash
# Export fresh data from cloud
python export_mongodb_data.py

# Import to local (overwrites existing data)
python import_mongodb_data.py
```

### Export from Local to Cloud (Not Recommended)

⚠️ **Note:** The cloud database user (`honeywell`) has read-only access, so you cannot push changes back to the cloud. This is by design for security.

---

## 🗂️ Database File Locations

### Exported JSON Files (Git-Tracked)
- Location: `data/mongodb_export/*.json`
- **✅ Committed to Git** (for team sharing)
- Small size (~few MB for 4,347 documents)

### Local MongoDB Data (Git-Ignored)
- Docker: Inside `mongodb_data` volume
- Linux: `/var/lib/mongodb/`
- macOS: `/usr/local/var/mongodb/`
- Windows: `C:\Program Files\MongoDB\Server\7.0\data\`
- **❌ NOT committed to Git** (too large, machine-specific)

---

## 🎯 Quick Reference

### Start Local MongoDB

**Docker:**
```bash
docker start mongodb-local
```

**Linux:**
```bash
sudo systemctl start mongod
```

**macOS:**
```bash
brew services start mongodb-community
```

### Stop Local MongoDB

**Docker:**
```bash
docker stop mongodb-local
```

**Linux:**
```bash
sudo systemctl stop mongod
```

**macOS:**
```bash
brew services stop mongodb-community
```

### Check if MongoDB is Running

```bash
# Try to connect
mongosh  # MongoDB Shell (if installed)

# Or use our test script
python test_mongodb_connection.py
```

---

## 🆘 Troubleshooting

### "Connection refused" Error

**Problem:** MongoDB is not running

**Solution:**
```bash
# Check if MongoDB is running
sudo systemctl status mongod  # Linux
brew services list  # macOS
docker ps  # Docker

# Start it if not running (see commands above)
```

### "Command not found: mongosh"

**Problem:** MongoDB Shell not installed (optional - not required)

**Solution:** You don't need it! Use our Python scripts instead:
```bash
python test_mongodb_connection.py
```

### Import Fails - "Export directory not found"

**Problem:** Haven't exported data yet

**Solution:**
```bash
python export_mongodb_data.py
```

### Local Database Empty

**Problem:** Imported but no data

**Solution:**
```bash
# Re-import
python import_mongodb_data.py
```

---

## 🔐 Permissions Comparison

| Feature | Cloud Database | Local Database |
|---------|---------------|----------------|
| Read Access | ✅ Yes | ✅ Yes |
| Write Access | ❌ No (read-only) | ✅ Yes |
| Insert Documents | ❌ Blocked | ✅ Allowed |
| Update Documents | ❌ Blocked | ✅ Allowed |
| Delete Documents | ❌ Blocked | ✅ Allowed |
| Create Collections | ❌ Blocked | ✅ Allowed |
| Cost | Free tier | Free (local) |
| Speed | Network latency | Very fast |
| Offline Access | ❌ No | ✅ Yes |

---

## 📝 Summary

1. ✅ Install MongoDB locally (Docker recommended)
2. ✅ Export cloud data: `python export_mongodb_data.py`
3. ✅ Import to local: `python import_mongodb_data.py`
4. ✅ Update `.env`: `MONGODB_URI=mongodb://localhost:27017/HoneyGo`
5. ✅ Verify: `python test_mongodb_connection.py`

**You're all set! 🎉**

Now you can develop with a fast local database and switch back to the cloud database anytime by updating your `.env` file.

