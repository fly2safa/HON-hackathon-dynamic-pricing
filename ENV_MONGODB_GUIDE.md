# MongoDB Configuration Guide for .env

Quick reference for configuring MongoDB in your `.env` file.

## 🔄 Switching Between Cloud and Local

### Option 1: Cloud MongoDB (Read-Only)

**Use when:**
- Need to access latest production data
- Testing read operations
- Don't need to modify data

**Add to .env:**
```bash
# Cloud MongoDB (read-only access)
MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority
```

### Option 2: Local MongoDB (Full Access)

**Use when:**
- Developing locally
- Need faster performance
- Want to test write operations
- Working offline

**Add to .env:**
```bash
# Local MongoDB (read/write access)
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

## 💡 Best Practice: Keep Both, Comment One Out

**In your `.env` file:**

```bash
# ============================================
# MongoDB Configuration
# ============================================
# Uncomment ONE of the following:

# OPTION 1: Cloud MongoDB (read-only)
# MONGODB_URI=mongodb+srv://honeywell:getyourcar@cluster0.qpxvnax.mongodb.net/HoneyGo?retryWrites=true&w=majority

# OPTION 2: Local MongoDB (read/write) - ACTIVE
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

**To switch:** Just move the `#` to the other line!

## ⚡ Quick Setup: Local MongoDB

### 1. Install MongoDB (One-Time)

**Docker (Recommended):**
```bash
docker run -d --name mongodb-local -p 27017:27017 -v mongodb_data:/data/db mongo:latest
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

### 2. Import Data (One-Time)

```bash
cd /home/jason/Python/AzNext_VibeCoding/HON-hackathon-dynamic-pricing
source venv/bin/activate
python import_mongodb_data.py
```

### 3. Update .env

```bash
# Edit .env and set:
MONGODB_URI=mongodb://localhost:27017/HoneyGo
```

### 4. Verify

```bash
python test_mongodb_connection.py
```

## 🔍 Database Info

### Cloud Database
- **Host:** cluster0.qpxvnax.mongodb.net
- **Database:** HoneyGo
- **User:** honeywell
- **Permissions:** Read-only
- **Collections:** 5
- **Documents:** 4,347

### Local Database
- **Host:** localhost:27017
- **Database:** HoneyGo
- **Permissions:** Full read/write
- **Collections:** 5 (after import)
- **Documents:** 4,347 (after import)

## 📊 Collections

Both databases have the same structure:

| Collection | Documents | Description |
|------------|-----------|-------------|
| customers | 988 | Customer profiles and loyalty data |
| rides | 1,000 | Ride requests and history |
| pricing_decisions | 1,000 | AI pricing decisions |
| drivers | 159 | Driver information |
| external_data | 1,200 | Weather, events, traffic data |

## 🆘 Troubleshooting

### "Connection refused" when using local

**Problem:** MongoDB is not running locally

**Solution:**
```bash
# Docker
docker start mongodb-local

# Linux
sudo systemctl start mongod

# macOS
brew services start mongodb-community
```

### "Authentication failed" when using cloud

**Problem:** Incorrect credentials or IP not whitelisted

**Solution:**
1. Verify credentials in MongoDB Atlas
2. Check IP whitelist in Atlas (Database Access → Network Access)

### "Database not found" on local

**Problem:** Haven't imported data yet

**Solution:**
```bash
python import_mongodb_data.py
```

## 📚 More Info

- **Full setup guide:** `MONGODB_LOCAL_SETUP.md`
- **Connection test:** `python test_mongodb_connection.py`
- **Read-only test:** `python test_mongodb_readonly.py`
- **Export data:** `python export_mongodb_data.py`
- **Import data:** `python import_mongodb_data.py`

