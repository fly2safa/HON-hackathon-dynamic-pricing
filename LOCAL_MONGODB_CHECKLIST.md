# ✅ Local MongoDB Setup Checklist

Follow these steps to set up local MongoDB on your laptop.

---

## ☑️ Step 1: Install MongoDB Locally

Choose **ONE** method:

### Option A: Docker (Recommended - Easiest)

```bash
# Pull and run MongoDB
docker run -d \
  --name mongodb-local \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# Verify it's running
docker ps | grep mongodb-local
```

**✅ Done when:** You see `mongodb-local` in docker ps output

---

### Option B: Native Installation

**Linux (Ubuntu/Debian):**
```bash
# Install
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify
sudo systemctl status mongod
```

**macOS:**
```bash
# Install
brew tap mongodb/brew
brew install mongodb-community

# Start
brew services start mongodb-community

# Verify
brew services list | grep mongodb
```

**✅ Done when:** MongoDB service is running

---

## ☑️ Step 2: Import Database

```bash
cd /home/jason/Python/AzNext_VibeCoding/HON-hackathon-dynamic-pricing

# Activate virtual environment
source venv/bin/activate

# Import data (this uses the JSON files already in data/mongodb_export/)
python import_mongodb_data.py
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
```

**✅ Done when:** All 5 collections show "imported" successfully

---

## ☑️ Step 3: Update .env File

Edit your `.env` file (create it if it doesn't exist):

```bash
nano .env
# or
code .env
# or
vim .env
```

Add these lines:

```bash
# ============================================
# MongoDB Configuration - CHOOSE ONE
# ============================================

# OPTION 1: Cloud MongoDB (read-only access)
# MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority

# OPTION 2: Local MongoDB (full read/write access)
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

**✅ Done when:** 
- `.env` file exists in project root
- `MONGODB_URI` is set to `mongodb://localhost:27017/HoneyGo`
- Cloud URI line is commented out with `#`

---

## ☑️ Step 4: Test Connection

```bash
# Still in venv
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

**✅ Done when:** All collections show the correct document counts

---

## ☑️ Step 5: Verify Read/Write Access

```bash
python test_mongodb_readonly.py
```

**Expected output for LOCAL (different from cloud!):**
```
📖 TESTING READ OPERATIONS (Should Succeed)
✅ All 5/5 read operations pass

🚫 TESTING WRITE OPERATIONS - Should SUCCEED on local
✅ Insert, Update, Delete all work (unlike cloud which blocks them)
```

**✅ Done when:** You see that write operations now WORK (not blocked)

---

## 🎉 Checklist Summary

- [ ] Step 1: MongoDB installed and running
- [ ] Step 2: Data imported successfully (4,347 documents)
- [ ] Step 3: .env file updated with local MongoDB URI
- [ ] Step 4: Connection test passed
- [ ] Step 5: Can perform read/write operations

---

## 🔄 Switching Between Cloud and Local

### To Switch to Cloud:

Edit `.env`:
```bash
# MONGODB_URI=mongodb://localhost:27017/HoneyGo  # ← Add # here
MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority  # ← Remove #
```

### To Switch Back to Local:

Edit `.env`:
```bash
MONGODB_URI=mongodb://localhost:27017/HoneyGo  # ← Remove # here
# MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority  # ← Add #
```

---

## 🆘 Troubleshooting

### ❌ "Connection refused" error

**Problem:** MongoDB not running

**Fix:**
```bash
# Docker
docker start mongodb-local

# Linux
sudo systemctl start mongod

# macOS
brew services start mongodb-community
```

### ❌ "Export directory not found"

**Problem:** Import script can't find JSON files

**Fix:**
```bash
# The files are already in Git at data/mongodb_export/
# Just make sure you're in the project root when running:
cd /home/jason/Python/AzNext_VibeCoding/HON-hackathon-dynamic-pricing
python import_mongodb_data.py
```

### ❌ "MONGODB_URI not found"

**Problem:** .env file doesn't exist or missing MONGODB_URI

**Fix:**
```bash
# Copy from example
cp env.example .env

# Then edit .env and add:
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

---

## 📚 Additional Resources

- **Full Setup Guide:** `MONGODB_LOCAL_SETUP.md`
- **ENV Reference:** `ENV_MONGODB_GUIDE.md`
- **Export Script:** `export_mongodb_data.py`
- **Import Script:** `import_mongodb_data.py`
- **Connection Test:** `test_mongodb_connection.py`
- **Security Test:** `test_mongodb_readonly.py`

---

## 💡 Tips

1. **Keep both URIs in .env** - Easy switching
2. **Use Docker** - Cleanest install/uninstall
3. **Re-export periodically** - Get fresh data from cloud
4. **Local for dev, cloud for prod** - Best practice

**Questions?** See `MONGODB_LOCAL_SETUP.md` for detailed explanations.

