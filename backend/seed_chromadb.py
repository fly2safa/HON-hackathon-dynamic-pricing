"""
Seed ChromaDB with Historical Ride Data

This script populates ChromaDB with the Honeywell dataset for RAG queries.
Run once to seed, then the data persists in ./chromadb_data/

Usage:
    cd backend
    python seed_chromadb.py
"""

import asyncio
import csv
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from services.chromadb_service import ChromaDBService


async def seed_from_csv():
    """Seed ChromaDB from the Honeywell CSV dataset"""
    
    print("🌱 ChromaDB Seeding Script")
    print("=" * 60)
    
    # Find the CSV file
    csv_paths = [
        "../project-spec/dynamic_pricing - dynamic_pricing.csv",
        "project-spec/dynamic_pricing - dynamic_pricing.csv",
        "./dynamic_pricing.csv"
    ]
    
    csv_path = None
    for path in csv_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        print("❌ CSV file not found! Tried:")
        for p in csv_paths:
            print(f"   - {p}")
        return
    
    print(f"📁 CSV file: {csv_path}")
    
    # Initialize ChromaDB
    service = ChromaDBService(persist_directory="./chromadb_data")
    await service.connect()
    
    # Check if already seeded
    stats = service.get_stats()
    if stats.get("collections", {}).get("rides", 0) > 0:
        existing = stats["collections"]["rides"]
        print(f"\n⚠️  ChromaDB already has {existing} rides!")
        response = input("Do you want to re-seed? This will add duplicates. (y/N): ")
        if response.lower() != 'y':
            print("✅ Keeping existing data. Done!")
            return
    
    # Read CSV
    rides = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rides.append({
                'number_of_riders': int(row.get('Number_of_Riders', 0)),
                'number_of_drivers': int(row.get('Number_of_Drivers', 0)),
                'location_category': row.get('Location_Category', ''),
                'customer_loyalty_status': row.get('Customer_Loyalty_Status', ''),
                'number_of_past_rides': int(row.get('Number_of_Past_Rides', 0)),
                'average_ratings': float(row.get('Average_Ratings', 0)),
                'time_of_booking': row.get('Time_of_Booking', ''),
                'vehicle_type': row.get('Vehicle_Type', ''),
                'expected_ride_duration': int(row.get('Expected_Ride_Duration', 0)),
                'historical_cost_of_ride': float(row.get('Historical_Cost_of_Ride', 0))
            })
    
    print(f"📊 Loaded {len(rides)} rides from CSV")
    
    # Seed ChromaDB
    print("\n🚀 Seeding ChromaDB...")
    added = await service.add_rides_batch(rides)
    
    # Verify
    stats = service.get_stats()
    print(f"\n✅ Seeding complete!")
    print(f"   Rides in ChromaDB: {stats['collections']['rides']}")
    print(f"   Persist directory: {stats['persist_directory']}")
    
    # Test query
    print("\n🔍 Testing query: 'Urban Premium ride at Night'")
    results = await service.query_similar_rides("Urban Premium ride at Night", n_results=3)
    
    if results:
        print(f"   Found {len(results)} similar rides:")
        for r in results:
            print(f"   - {r['text'][:80]}... (similarity: {r['similarity']:.2f})")
    else:
        print("   No results (this shouldn't happen after seeding)")
    
    print("\n🎉 Done! ChromaDB is ready for RAG queries.")


if __name__ == "__main__":
    asyncio.run(seed_from_csv())

