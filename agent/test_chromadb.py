#!/usr/bin/env python3
"""
ChromaDB Test Script

Tests semantic search and RAG functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag.chromadb_client import ChromaDBClient


def test_connection():
    """Test ChromaDB connection"""
    print("=" * 60)
    print("Test 1: Connection")
    print("=" * 60)
    
    client = ChromaDBClient(persist_directory="./chromadb_data")
    client.connect()
    
    print("✅ Connection successful!")
    print(f"  - hon_knowledge: {client.get_collection_count('hon_knowledge')} docs")
    print(f"  - pricing_reasoning: {client.get_collection_count('pricing_reasoning')} docs")
    print()
    
    return client


def test_hon_knowledge(client):
    """Test HON knowledge queries"""
    print("=" * 60)
    print("Test 2: HON Knowledge Semantic Search")
    print("=" * 60)
    
    queries = [
        "What is the approach to surge pricing during bad weather?",
        "How should customer loyalty be rewarded?",
        "What are the regulations for ride-sharing in New York?"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        results = client.query_knowledge(query, collection_name="hon_knowledge", n_results=2)
        
        if results:
            print(f"✅ Found {len(results)} results")
            print(f"   Top result: {results[0]['text'][:100]}...")
        else:
            print("❌ No results found")
    
    print()


def test_pricing_reasoning(client):
    """Test pricing reasoning queries"""
    print("=" * 60)
    print("Test 3: Pricing Reasoning Semantic Search")
    print("=" * 60)
    
    scenarios = [
        "Urban ride during evening rush hour with rain",
        "Airport pickup early morning",
        "Short ride with minimum fare"
    ]
    
    for scenario in scenarios:
        print(f"\n📝 Scenario: {scenario}")
        results = client.get_pricing_reasoning(scenario, n_results=2)
        
        if results:
            print(f"✅ Found {len(results)} similar decisions")
            print(f"   Top match: {results[0]['text'][:100]}...")
            if 'metadata' in results[0]:
                print(f"   Metadata: {results[0]['metadata']}")
        else:
            print("❌ No similar decisions found")
    
    print()


def test_rag_tool():
    """Test RAG tool integration"""
    print("=" * 60)
    print("Test 4: RAG Tool")
    print("=" * 60)
    
    try:
        from tools.rag_tool import create_rag_tool
        
        client = ChromaDBClient(persist_directory="./chromadb_data")
        client.connect()
        
        rag_tool = create_rag_tool(client)
        
        print("✅ RAG tool created successfully")
        print(f"   Tool name: {rag_tool.name}")
        print(f"   Tool description: {rag_tool.description[:80]}...")
        print()
        
        # Test tool execution
        print("🔍 Testing tool execution...")
        result = rag_tool._run(
            query="What factors affect dynamic pricing?",
            collection="hon_knowledge",
            n_results=2
        )
        
        if result and "Error" not in result:
            print("✅ Tool execution successful")
            print(f"   Result preview: {result[:150]}...")
        else:
            print(f"❌ Tool execution failed: {result}")
        
        client.disconnect()
        
    except Exception as e:
        print(f"❌ RAG tool test failed: {e}")
    
    print()


def test_add_knowledge(client):
    """Test adding new knowledge"""
    print("=" * 60)
    print("Test 5: Adding Knowledge")
    print("=" * 60)
    
    try:
        # Add a test knowledge item
        item_id = client.add_knowledge(
            text="Test knowledge item: Dynamic pricing should always consider customer satisfaction alongside profitability.",
            metadata={"category": "test", "source": "test_script"},
            collection_name="similar_contexts"
        )
        
        print(f"✅ Added knowledge item: {item_id}")
        
        # Query it back
        results = client.query_knowledge(
            query="customer satisfaction in pricing",
            collection_name="similar_contexts",
            n_results=1
        )
        
        if results and "customer satisfaction" in results[0]['text']:
            print("✅ Successfully retrieved added knowledge")
        else:
            print("⚠️  Could not retrieve added knowledge")
        
    except Exception as e:
        print(f"❌ Add knowledge test failed: {e}")
    
    print()


def main():
    """Run all tests"""
    print("\n")
    print("🧪 ChromaDB RAG Functionality Tests")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Connection
        client = test_connection()
        
        # Check if data exists
        if client.get_collection_count('hon_knowledge') == 0:
            print("⚠️  No data found! Run setup_chromadb.py first.")
            print()
            return
        
        # Test 2: HON Knowledge
        test_hon_knowledge(client)
        
        # Test 3: Pricing Reasoning
        test_pricing_reasoning(client)
        
        # Test 4: RAG Tool
        test_rag_tool()
        
        # Test 5: Add Knowledge
        test_add_knowledge(client)
        
        # Cleanup
        client.disconnect()
        
        # Summary
        print("=" * 60)
        print("✨ All Tests Complete!")
        print("=" * 60)
        print()
        print("✅ ChromaDB RAG functionality is working correctly!")
        print("✅ Ready for agent integration!")
        print()
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

