"""
Export MongoDB Data from Cloud Database
Exports all collections to JSON files for local import
"""
import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

def export_database():
    """Export all collections from MongoDB to JSON files"""
    
    mongodb_uri = os.getenv("MONGODB_URI")
    
    if not mongodb_uri:
        print("❌ ERROR: MONGODB_URI not found in .env file")
        return
    
    print("📦 Exporting MongoDB Data")
    print("=" * 70)
    print(f"📍 Source: {mongodb_uri[:50]}...")
    
    # Create export directory
    export_dir = Path("data/mongodb_export")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Connected to cloud database\n")
        
        # Get database name from URI
        db_name = mongodb_uri.split('/')[-1].split('?')[0]
        db = client[db_name]
        
        # Get all collections
        try:
            collections = db.list_collection_names()
        except:
            # If list_collections is restricted, use known collections
            collections = ['customers', 'rides', 'pricing_decisions', 'drivers', 'external_data']
        
        print(f"📚 Database: {db_name}")
        print(f"📁 Export directory: {export_dir}\n")
        
        total_documents = 0
        exported_collections = []
        
        # Export each collection
        for collection_name in collections:
            try:
                collection = db[collection_name]
                
                # Get all documents (excluding MongoDB's _id field)
                documents = list(collection.find({}, {"_id": 0}))
                
                if not documents:
                    print(f"⚠️  {collection_name}: Empty collection, skipping")
                    continue
                
                # Save to JSON file
                output_file = export_dir / f"{collection_name}.json"
                with open(output_file, 'w') as f:
                    json.dump(documents, f, indent=2, default=str)
                
                total_documents += len(documents)
                exported_collections.append(collection_name)
                
                print(f"✅ {collection_name}: {len(documents)} documents → {output_file.name}")
                
            except Exception as e:
                print(f"❌ {collection_name}: Failed - {str(e)}")
        
        # Create metadata file
        metadata = {
            "export_date": datetime.now().isoformat(),
            "source_database": db_name,
            "total_collections": len(exported_collections),
            "total_documents": total_documents,
            "collections": {
                name: len(list(db[name].find({}, {"_id": 0}))) 
                for name in exported_collections
            }
        }
        
        metadata_file = export_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📊 Export Summary:")
        print(f"  Collections exported: {len(exported_collections)}")
        print(f"  Total documents: {total_documents}")
        print(f"  Export location: {export_dir}")
        print(f"  Metadata: {metadata_file.name}")
        
        print("\n✅ Export completed successfully!")
        print("\n💡 Next steps:")
        print("  1. Install MongoDB locally (see MONGODB_LOCAL_SETUP.md)")
        print("  2. Run: python import_mongodb_data.py")
        print("  3. Update .env with local MongoDB URI")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    export_database()

