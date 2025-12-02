"""
Test MongoDB Connection and List Collections
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB connection and list all collections with document counts"""
    
    mongodb_uri = os.getenv("MONGODB_URI")
    
    if not mongodb_uri:
        print("❌ ERROR: MONGODB_URI not found in .env file")
        return
    
    print("🔗 Testing MongoDB connection...")
    print(f"📍 Connection URI: {mongodb_uri[:50]}...")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection with ping
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Extract database name from URI
        # Format: mongodb+srv://user:pass@host/DATABASE?params
        db_name = mongodb_uri.split('/')[-1].split('?')[0]
        print(f"\n📚 Database specified in URI: {db_name}")
        
        # Try both database names
        databases_to_test = [db_name]
        if db_name != "honeygo":
            databases_to_test.append("honeygo")
        
        for test_db_name in databases_to_test:
            print(f"\n{'='*60}")
            print(f"Testing database: {test_db_name}")
            print('='*60)
            test_database(client, test_db_name)
        
        # Close connection
        client.close()
        print("\n✅ Connection test completed successfully!")
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Possible issues:")
        print("  - Check your username and password")
        print("  - Verify your IP address is whitelisted in MongoDB Atlas")
        print("  - Ensure the cluster is running")
        
    except OperationFailure as e:
        print(f"❌ Operation failed: {e}")
        print("\n💡 Possible issues:")
        print("  - User may not have read permissions")
        print("  - Database name might be incorrect")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_database(client, db_name):
    """Test access to a specific database"""
    db = client[db_name]
    
    try:
        
        # Try to list collections (may fail with read-only permissions)
        try:
            collections = db.list_collection_names()
            print(f"\n📊 Found {len(collections)} collection(s):")
            for coll in collections:
                print(f"  - {coll}")
        except OperationFailure as e:
            print(f"\n⚠️  Cannot list collections (permission restricted): {e.details.get('errmsg', str(e))}")
            print("📌 Trying known collection names instead...")
            collections = ['rides', 'customers', 'drivers', 'pricing_decisions', 'external_data']
        
        # Try to access and count documents in each collection
        print(f"\n📊 Checking collections:\n")
        total_docs = 0
        accessible_collections = []
        
        for collection_name in collections:
            try:
                count = db[collection_name].count_documents({})
                total_docs += count
                accessible_collections.append(collection_name)
                print(f"  ✅ {collection_name}: {count} documents")
            except OperationFailure as e:
                print(f"  ❌ {collection_name}: No access - {e.details.get('errmsg', 'Permission denied')}")
            except Exception as e:
                print(f"  ⚠️  {collection_name}: Error - {str(e)}")
        
        if total_docs > 0:
            print(f"\n📈 Total documents across accessible collections: {total_docs}")
            
            # Show sample document from first non-empty collection
            for collection_name in accessible_collections:
                try:
                    if db[collection_name].count_documents({}) > 0:
                        print(f"\n🔍 Sample document from '{collection_name}':")
                        sample = db[collection_name].find_one({}, {"_id": 0})
                        
                        # Print first few fields
                        if sample:
                            for i, (key, value) in enumerate(list(sample.items())[:5]):
                                print(f"    {key}: {value}")
                            if len(sample) > 5:
                                print(f"    ... ({len(sample) - 5} more fields)")
                        break
                except Exception as e:
                    print(f"  ⚠️  Could not read sample: {e}")
                    continue
        else:
            print("\n💡 No documents found in any accessible collections")
    
    except OperationFailure as e:
        print(f"❌ Operation failed on database '{db_name}': {e.details.get('errmsg', str(e))}")
    except Exception as e:
        print(f"❌ Unexpected error on database '{db_name}': {e}")

if __name__ == "__main__":
    test_connection()

