#!/usr/bin/env python3
"""
ChromaDB Setup Script

Initializes ChromaDB and seeds it with HON knowledge and pricing reasoning.
Run this once before using the agent.
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag.chromadb_client import ChromaDBClient
from rag.knowledge_base import seed_all

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main setup function"""
    print("=" * 60)
    print("ChromaDB Setup for HoneyGo Pricing Agent")
    print("=" * 60)
    print()
    
    # Initialize client
    print("📦 Initializing ChromaDB client...")
    client = ChromaDBClient(persist_directory="./chromadb_data")
    
    # Connect
    print("🔌 Connecting to ChromaDB...")
    client.connect()
    print("✅ Connected successfully!")
    print()
    
    # Check existing data
    print("📊 Checking existing collections...")
    hon_count = client.get_collection_count("hon_knowledge")
    pricing_count = client.get_collection_count("pricing_reasoning")
    context_count = client.get_collection_count("similar_contexts")
    
    print(f"  - hon_knowledge: {hon_count} documents")
    print(f"  - pricing_reasoning: {pricing_count} documents")
    print(f"  - similar_contexts: {context_count} documents")
    print()
    
    # Ask about clearing
    if hon_count > 0 or pricing_count > 0:
        response = input("⚠️  Existing data found. Clear and reseed? (y/n): ").strip().lower()
        clear_existing = response == 'y'
    else:
        clear_existing = False
        print("📝 No existing data found. Proceeding with seeding...")
    
    print()
    
    # Seed data
    print("🌱 Seeding knowledge bases...")
    results = seed_all(client, clear_existing=clear_existing)
    print()
    
    # Summary
    print("=" * 60)
    print("✨ Setup Complete!")
    print("=" * 60)
    print()
    print("📊 Summary:")
    print(f"  - HON Knowledge: {results['hon_knowledge']} items")
    print(f"  - Pricing Reasoning: {results['pricing_reasoning']} items")
    print()
    
    # Verify with a test query
    print("🔍 Testing semantic search...")
    test_results = client.query_knowledge(
        query="What is the approach to surge pricing during bad weather?",
        collection_name="hon_knowledge",
        n_results=2
    )
    
    if test_results:
        print(f"✅ Test successful! Found {len(test_results)} relevant results.")
        print()
        print("Sample result:")
        print(f"  {test_results[0]['text'][:150]}...")
    else:
        print("⚠️  Test query returned no results. Check your setup.")
    
    print()
    print("=" * 60)
    print("🚀 ChromaDB is ready! You can now run the agent.")
    print("=" * 60)
    
    # Disconnect
    client.disconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed: {e}", exc_info=True)
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

