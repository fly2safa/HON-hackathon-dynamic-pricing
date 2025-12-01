# HoneyGo Agent Setup Guide

## Required Accounts & API Keys

### 1. OpenAI API Key (Required)
**What:** LLM for the pricing agent  
**Cost:** Pay-as-you-go (~$0.01-0.03 per pricing decision with GPT-4)  
**Free Tier:** $5 credit for new accounts

**Steps:**
1. Go to https://platform.openai.com/signup
2. Create account
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)
6. Add to `agent/.env`: `OPENAI_API_KEY=sk-your-key-here`

**Alternative:** Use Claude (Anthropic) instead - similar pricing

---

### 2. LangSmith API Key (Highly Recommended)
**What:** AI agent observability platform - see how the agent thinks!  
**Cost:** FREE tier (5,000 traces/month - plenty for hackathon)  
**Why:** Judges will be impressed seeing real-time agent reasoning

**Steps:**
1. Go to https://smith.langchain.com/
2. Sign up (can use GitHub login)
3. Create a new project: "honeygo-pricing"
4. Go to Settings → API Keys
5. Create new API key
6. Add to `agent/.env`:
   ```
   LANGSMITH_API_KEY=lsv2_pt_your-key-here
   LANGSMITH_PROJECT=honeygo-pricing
   LANGSMITH_TRACING=true
   ```

**View traces at:** https://smith.langchain.com/

---

### 3. MongoDB (Required for Production, Optional for Testing)
**What:** Database for storing rides and pricing decisions  
**Cost:** FREE (MongoDB Atlas free tier or local)

**Option A: Local (Easiest for Development)**
1. Install MongoDB Community: https://www.mongodb.com/try/download/community
2. Run: `mongod`
3. Use: `MONGODB_URI=mongodb://localhost:27017/honeygo_pricing`

**Option B: MongoDB Atlas (Cloud - FREE)**
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free cluster (M0 tier)
3. Get connection string
4. Add to `.env`: `MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/honeygo_pricing`

---

### 4. ChromaDB (Optional for Now)
**What:** Vector database for RAG (semantic search)  
**Cost:** FREE (local or cloud)

**Local Setup:**
```bash
pip install chromadb
# Runs on localhost:8000 by default
```

---

## Quick Start

### 1. Copy Environment File
```bash
cd agent
cp env.example .env
```

### 2. Add Your API Keys
Edit `agent/.env` and add:
- OpenAI API key (required)
- LangSmith API key (highly recommended)
- MongoDB URI (optional for testing)

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test the Agent
```bash
cd src
python agent.py
```

You should see:
```
✅ LangSmith observability enabled - Project: honeygo-pricing
✅ HoneyGo Pricing Agent initialized
   Model: gpt-4-turbo-preview
   Tools: 3
   LangSmith: Enabled
```

---

## Cost Estimate for Hackathon

**Total: ~$5-10 for entire hackathon**

- **OpenAI API**: $3-5 (100-200 pricing calculations)
- **LangSmith**: FREE (under 5,000 traces)
- **MongoDB**: FREE (Atlas M0 tier)
- **ChromaDB**: FREE (local)

**Tip:** OpenAI gives $5 free credit to new accounts - might cover entire hackathon!

---

## Troubleshooting

### "OpenAI API key not found"
- Make sure `.env` file exists in `agent/` folder
- Check key starts with `sk-`
- Restart terminal after adding key

### "LangSmith not showing traces"
- Verify `LANGSMITH_TRACING=true` in `.env`
- Check project name matches in LangSmith dashboard
- Wait 5-10 seconds for traces to appear

### "MongoDB connection failed"
- For local: Make sure `mongod` is running
- For Atlas: Check connection string and whitelist your IP

---

## Team Member Setup

**For Dari (Backend Integration):**
- She doesn't need these keys in her backend
- Backend will call your agent as a module
- Keys stay in `agent/.env` only

**For Demo Day:**
- Use your API keys
- LangSmith dashboard open on second screen
- Show judges the agent reasoning in real-time!

---

## Next Steps After Setup

1. Test agent with `python agent.py`
2. View traces in LangSmith dashboard
3. Coordinate with Dari on FastAPI integration
4. Add more tools as needed
5. Test with real MongoDB when Jason's database is ready

