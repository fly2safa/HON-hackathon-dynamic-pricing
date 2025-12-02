# ChromaDB Setup Guide

## Overview

ChromaDB provides **RAG (Retrieval-Augmented Generation)** capabilities for the HoneyGo pricing agent. It enables semantic search across:

- **HON Knowledge**: Honeywell domain knowledge and best practices (25 items)
- **Pricing Reasoning**: Historical pricing decisions with detailed reasoning (10 examples)
- **Similar Contexts**: Contextually similar situations for pattern matching

## Prerequisites

1. **Python 3.10+** installed
2. **Agent dependencies** installed:
   ```bash
   cd agent
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Run Setup Script

From the `agent/` directory:

```bash
python setup_chromadb.py
```

This will:
- Initialize ChromaDB with persistent storage
- Create 3 collections (hon_knowledge, pricing_reasoning, similar_contexts)
- Seed 25 HON knowledge items
- Seed 10 pricing reasoning examples
- Test semantic search functionality

### 2. Verify Setup

The script will test a sample query. You should see:

```
✅ Test successful! Found 2 relevant results.

Sample result:
  Weather conditions significantly impact ride demand and pricing...
```

## What Gets Seeded

### HON Knowledge (25 Items)

Categories:
- **Pricing Philosophy**: Value-based strategies, customer relationships
- **Weather Impact**: Rain (+20-30%), Snow (+40-50%), Severe (+60%+)
- **Loyalty Program**: Bronze/Silver/Gold/Platinum tiers with discounts
- **Geographic Pricing**: Urban/Suburban/Rural adjustments
- **Time-Based Pricing**: Rush hours, late night, weekend surges
- **Event Impact**: Concerts, sports, conventions
- **Competitor Analysis**: Market positioning strategies
- **Regulations**: Phoenix, New York, San Francisco compliance
- **Customer Communication**: Transparency best practices
- **Minimum/Maximum Policies**: Fare limits and caps
- **AI Confidence**: Governance and review thresholds
- **Seasonal Adjustments**: Summer/Winter/Holiday pricing
- **Traffic Impact**: Real-time optimization
- **Data Privacy**: GDPR, CCPA compliance
- **Experimentation**: A/B testing strategies

### Pricing Reasoning (10 Examples)

Scenarios covered:
1. Urban evening + rain + Gold customer
2. Suburban morning + clear + Bronze customer
3. Urban late night + concert + Platinum customer
4. Urban midday + snow + Silver customer
5. Airport early morning + clear + Gold customer
6. Short urban ride + minimum fare
7. Scheduled advance booking + Silver customer
8. Multi-passenger (5 people) + Bronze customer
9. Rural evening + minimum fare
10. Weekend night + entertainment district

Each example includes:
- Full pricing breakdown
- Reasoning explanation
- Scenario metadata
- Outcome status

## Using ChromaDB in Your Code

### Initialize Client

```python
from rag.chromadb_client import ChromaDBClient

client = ChromaDBClient(persist_directory="./chromadb_data")
client.connect()
```

### Query Knowledge

```python
# Query HON knowledge
results = client.query_knowledge(
    query="What is the approach to surge pricing during weather events?",
    collection_name="hon_knowledge",
    n_results=3
)

for result in results:
    print(result['text'])
    print(result['metadata'])
```

### Get Similar Pricing Reasoning

```python
# Find similar historical decisions
scenario = "Urban ride, 8 miles, evening rush, rainy weather, Gold customer"
similar = client.get_pricing_reasoning(scenario, n_results=3)

for decision in similar:
    print(decision['text'])
```

### Add New Knowledge

```python
# Add a new knowledge item
client.add_knowledge(
    text="New pricing insight or best practice...",
    metadata={"category": "custom", "source": "team"},
    collection_name="hon_knowledge"
)
```

### Add Pricing Decision

```python
# Store a new pricing decision
client.add_pricing_decision(
    decision_text="Ride details and reasoning...",
    metadata={
        "distance_miles": 10,
        "final_price": 25.50,
        "customer_tier": "gold"
    }
)
```

## Using RAG Tool in LangChain Agent

```python
from tools import create_rag_tool
from rag.chromadb_client import ChromaDBClient

# Initialize ChromaDB
chroma_client = ChromaDBClient()
chroma_client.connect()

# Create RAG tool
rag_tool = create_rag_tool(chroma_client)

# Add to agent tools
tools = [
    pricing_calculator_tool,
    database_tool,
    weather_tool,
    rag_tool  # ← RAG tool for knowledge retrieval
]

# Agent can now use semantic search!
```

## Agent Usage Example

When the agent runs, it can use the RAG tool:

```
Agent: I need to price an urban ride during rain with a Gold customer.
Let me check HON knowledge for weather pricing guidance.

Action: semantic_knowledge_retrieval
Action Input: {
  "query": "weather impact on pricing during rain",
  "collection": "hon_knowledge",
  "n_results": 2
}

Observation: Found 2 relevant knowledge items:
[Result 1]
Content: Weather conditions significantly impact ride demand and pricing. 
Rain increases demand by 20-30%, snow by 40-50%...
Metadata: category: weather_impact, relevance: high

[Result 2]
Content: Dynamic pricing should balance profitability with partner retention...
Metadata: category: partner_retention, relevance: high

Thought: Based on HON knowledge, rain increases demand by 20-30%. 
I should apply a 1.2-1.3x multiplier...
```

## Data Persistence

ChromaDB data is stored in `./chromadb_data/` directory:

```
chromadb_data/
├── chroma.sqlite3        # Metadata database
└── [embedding files]     # Vector embeddings
```

**Important:**
- ✅ Data persists across agent restarts
- ✅ No need to reseed unless you want to update knowledge
- ⚠️ Add `chromadb_data/` to `.gitignore` (already done)

## Updating Knowledge

### Option 1: Reseed Everything

```bash
python setup_chromadb.py
# Answer 'y' when prompted to clear existing data
```

### Option 2: Add Incrementally

```python
from rag.chromadb_client import ChromaDBClient

client = ChromaDBClient()
client.connect()

# Add new knowledge without clearing
client.add_knowledge(
    text="Your new knowledge item...",
    metadata={"category": "new_category"},
    collection_name="hon_knowledge"
)
```

## Troubleshooting

### Issue: "No module named 'chromadb'"

**Solution:**
```bash
pip install chromadb==0.4.22 sentence-transformers==2.2.2
```

### Issue: "Collection not available"

**Solution:** Run the setup script first:
```bash
python setup_chromadb.py
```

### Issue: Slow first query

**Explanation:** The first query downloads the sentence-transformer model (~80MB). Subsequent queries are fast.

**Solution:** Wait for the initial download to complete. It only happens once.

### Issue: "Permission denied" on chromadb_data/

**Solution:** Check folder permissions:
```bash
chmod -R 755 chromadb_data/
```

### Issue: Want to reset everything

**Solution:**
```bash
rm -rf chromadb_data/
python setup_chromadb.py
```

## Performance

- **Initial Setup**: ~30-60 seconds (includes model download)
- **Query Time**: ~50-200ms per query
- **Storage**: ~5-10 MB for 35 documents
- **Memory**: ~200-300 MB (for embedding model)

## Architecture

```
Agent
  ↓
RAG Tool (rag_tool.py)
  ↓
ChromaDB Client (chromadb_client.py)
  ↓
ChromaDB (persistent storage)
  ├── hon_knowledge (25 items)
  ├── pricing_reasoning (10 items)
  └── similar_contexts (empty, for future use)
```

## Next Steps

1. ✅ Run `python setup_chromadb.py`
2. ✅ Verify test query succeeds
3. ✅ Integrate RAG tool into agent
4. ✅ Test agent with knowledge retrieval
5. 🔄 Add more knowledge as needed

## Questions?

- Check `agent/src/rag/` for implementation details
- See `agent/src/tools/rag_tool.py` for tool usage
- Review `agent/src/rag/knowledge_base.py` for seeding logic

---

**Ready to use RAG!** 🚀

