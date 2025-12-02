"""
Import MongoDB Data to Local Database
Imports all collections from JSON files into local MongoDB
"""
import os
import json
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def import_database(local_uri="mongodb://localhost:27017/", db_name="HoneyGo"):
    """Import all collections from JSON files to local MongoDB"""
    
    print("📥 Importing MongoDB Data to Local Database")
    print("=" * 70)
    print(f"📍 Target: {local_uri}{db_name}")
    
    # Check if export directory exists
    export_dir = Path("data/mongodb_export")
    if not export_dir.exists():
        print(f"❌ ERROR: Export directory not found: {export_dir}")
        print("💡 Run: python export_mongodb_data.py first")
        return
    
    # Check if there are any JSON files
    json_files = list(export_dir.glob("*.json"))
    if not json_files:
        print(f"❌ ERROR: No JSON files found in {export_dir}")
        print("💡 Run: python export_mongodb_data.py first")
        return
    
    # Remove metadata.json from the list
    json_files = [f for f in json_files if f.name != "metadata.json"]
    
    try:
        # Connect to local MongoDB
        print("\n🔗 Connecting to local MongoDB...")
        client = MongoClient(local_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Connected to local MongoDB\n")
        
        # Get or create database
        db = client[db_name]
        
        print(f"📚 Database: {db_name}")
        print(f"📁 Import directory: {export_dir}\n")
        
        total_documents = 0
        imported_collections = []
        
        # Import each collection
        for json_file in json_files:
            collection_name = json_file.stem
            
            try:
                # Read JSON file
                with open(json_file, 'r') as f:
                    documents = json.load(f)
                
                if not documents:
                    print(f"⚠️  {collection_name}: No documents in file, skipping")
                    continue
                
                # Drop existing collection if it exists (clean import)
                if collection_name in db.list_collection_names():
                    db[collection_name].drop()
                    print(f"🗑️  {collection_name}: Dropped existing collection")
                
                # Insert documents
                collection = db[collection_name]
                result = collection.insert_many(documents)
                
                total_documents += len(result.inserted_ids)
                imported_collections.append(collection_name)
                
                print(f"✅ {collection_name}: {len(result.inserted_ids)} documents imported")
                
            except Exception as e:
                print(f"❌ {collection_name}: Failed - {str(e)}")
        
        # Verify import
        print(f"\n📊 Import Summary:")
        print(f"  Collections imported: {len(imported_collections)}")
        print(f"  Total documents: {total_documents}")
        print(f"\n🔍 Verification:")
        
        for collection_name in imported_collections:
            count = db[collection_name].count_documents({})
            print(f"  ✅ {collection_name}: {count} documents")
        
        print("\n✅ Import completed successfully!")
        print("\n💡 Next steps:")
        print("  1. Add to .env file:")
        print(f"     MONGODB_URI={local_uri}{db_name}")
        print("  2. Restart your application")
        print("  3. Run: python test_mongodb_connection.py to verify")
        
        client.close()
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure MongoDB is running locally:")
        print("  - macOS: brew services start mongodb-community")
        print("  - Linux: sudo systemctl start mongod")
        print("  - Windows: net start MongoDB")
        print("  - Docker: docker run -d -p 27017:27017 --name mongodb mongo:latest")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Import MongoDB data from JSON files')
    parser.add_argument('--uri', default='mongodb://localhost:27017/', 
                       help='MongoDB connection URI (default: mongodb://localhost:27017/)')
    parser.add_argument('--db', default='HoneyGo', 
                       help='Database name (default: HoneyGo)')
    
    args = parser.parse_args()
    
    import_database(args.uri, args.db)

