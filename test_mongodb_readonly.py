"""
Test MongoDB Read-Only Permissions
Verifies that the user can only read data and cannot create, update, or delete
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime

# Load environment variables
load_dotenv()

def test_readonly_permissions():
    """Test that MongoDB user has read-only access (no write permissions)"""
    
    mongodb_uri = os.getenv("MONGODB_URI")
    
    if not mongodb_uri:
        print("❌ ERROR: MONGODB_URI not found in .env file")
        return
    
    print("🔒 Testing MongoDB Read-Only Permissions")
    print("=" * 70)
    print(f"📍 Connection URI: {mongodb_uri[:50]}...")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection with ping
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!\n")
        
        # Extract database name from URI
        db_name = mongodb_uri.split('/')[-1].split('?')[0]
        db = client[db_name]
        
        print(f"📚 Testing Database: {db_name}")
        print("=" * 70)
        
        # Test results tracker
        read_tests_passed = 0
        write_tests_blocked = 0
        
        # =====================================================================
        # READ OPERATIONS (Should Work)
        # =====================================================================
        print("\n📖 TESTING READ OPERATIONS (Should Succeed)")
        print("-" * 70)
        
        # Test 1: List Collections (may fail with read-only)
        try:
            collections = db.list_collection_names()
            print(f"✅ List Collections: SUCCESS ({len(collections)} collections)")
            read_tests_passed += 1
        except OperationFailure as e:
            print(f"⚠️  List Collections: RESTRICTED (this is OK for read-only)")
        
        # Test 2: Count Documents
        try:
            count = db.customers.count_documents({})
            print(f"✅ Count Documents (customers): SUCCESS ({count} documents)")
            read_tests_passed += 1
        except OperationFailure as e:
            print(f"❌ Count Documents: FAILED - {e.details.get('errmsg', str(e))}")
        
        # Test 3: Find One Document
        try:
            doc = db.customers.find_one({}, {"_id": 0})
            if doc:
                print(f"✅ Find One Document: SUCCESS (found customer: {doc.get('customer_id', 'N/A')})")
                read_tests_passed += 1
            else:
                print("⚠️  Find One Document: No documents found")
        except OperationFailure as e:
            print(f"❌ Find One Document: FAILED - {e.details.get('errmsg', str(e))}")
        
        # Test 4: Find Multiple Documents
        try:
            docs = list(db.rides.find({}).limit(5))
            print(f"✅ Find Multiple Documents: SUCCESS ({len(docs)} rides retrieved)")
            read_tests_passed += 1
        except OperationFailure as e:
            print(f"❌ Find Multiple Documents: FAILED - {e.details.get('errmsg', str(e))}")
        
        # Test 5: Query with Filter
        try:
            gold_customers = db.customers.count_documents({"loyalty_status": "Gold"})
            print(f"✅ Query with Filter: SUCCESS ({gold_customers} Gold customers)")
            read_tests_passed += 1
        except OperationFailure as e:
            print(f"❌ Query with Filter: FAILED - {e.details.get('errmsg', str(e))}")
        
        # =====================================================================
        # WRITE OPERATIONS - INSERT (Should Fail)
        # =====================================================================
        print("\n\n🚫 TESTING WRITE OPERATIONS - INSERT (Should Be Blocked)")
        print("-" * 70)
        
        # Test 6: Insert One Document
        try:
            test_doc = {
                "test_id": "TEST-001",
                "test_field": "This is a test",
                "created_at": datetime.utcnow(),
                "note": "This should NOT be inserted if read-only"
            }
            result = db.test_collection.insert_one(test_doc)
            print(f"❌ SECURITY ISSUE: Insert One SUCCEEDED (id: {result.inserted_id})")
            print("   ⚠️  WARNING: User has WRITE permissions! Not read-only!")
        except OperationFailure as e:
            print(f"✅ Insert One: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # Test 7: Insert Many Documents
        try:
            test_docs = [
                {"test_id": "TEST-002", "value": 1},
                {"test_id": "TEST-003", "value": 2}
            ]
            result = db.test_collection.insert_many(test_docs)
            print(f"❌ SECURITY ISSUE: Insert Many SUCCEEDED ({len(result.inserted_ids)} docs)")
            print("   ⚠️  WARNING: User has WRITE permissions! Not read-only!")
        except OperationFailure as e:
            print(f"✅ Insert Many: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # =====================================================================
        # WRITE OPERATIONS - UPDATE (Should Fail)
        # =====================================================================
        print("\n\n🚫 TESTING WRITE OPERATIONS - UPDATE (Should Be Blocked)")
        print("-" * 70)
        
        # Test 8: Update One Document
        try:
            result = db.customers.update_one(
                {"customer_id": "CUST-001"},
                {"$set": {"test_field": "Modified by test"}}
            )
            if result.modified_count > 0:
                print(f"❌ SECURITY ISSUE: Update One SUCCEEDED (modified {result.modified_count} docs)")
                print("   ⚠️  WARNING: User has WRITE permissions! Not read-only!")
            else:
                print(f"❌ SECURITY ISSUE: Update One ALLOWED but no docs matched")
        except OperationFailure as e:
            print(f"✅ Update One: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # Test 9: Update Many Documents
        try:
            result = db.customers.update_many(
                {"loyalty_status": "Gold"},
                {"$set": {"test_modified": True}}
            )
            if result.modified_count > 0:
                print(f"❌ SECURITY ISSUE: Update Many SUCCEEDED (modified {result.modified_count} docs)")
                print("   ⚠️  WARNING: User has WRITE permissions! Not read-only!")
            else:
                print(f"❌ SECURITY ISSUE: Update Many ALLOWED but no docs matched")
        except OperationFailure as e:
            print(f"✅ Update Many: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # Test 10: Replace One Document
        try:
            result = db.customers.replace_one(
                {"customer_id": "CUST-001"},
                {"customer_id": "CUST-001", "replaced": True}
            )
            if result.modified_count > 0:
                print(f"❌ SECURITY ISSUE: Replace One SUCCEEDED")
                print("   ⚠️  WARNING: User has WRITE permissions! Not read-only!")
            else:
                print(f"❌ SECURITY ISSUE: Replace One ALLOWED but no docs matched")
        except OperationFailure as e:
            print(f"✅ Replace One: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # =====================================================================
        # WRITE OPERATIONS - DELETE (Should Fail)
        # =====================================================================
        print("\n\n🚫 TESTING WRITE OPERATIONS - DELETE (Should Be Blocked)")
        print("-" * 70)
        
        # Test 11: Delete One Document
        try:
            result = db.customers.delete_one({"customer_id": "CUST-999999"})
            if result.deleted_count > 0:
                print(f"❌ SECURITY ISSUE: Delete One SUCCEEDED (deleted {result.deleted_count} docs)")
                print("   ⚠️  WARNING: User has DELETE permissions! Not read-only!")
            else:
                print(f"❌ SECURITY ISSUE: Delete One ALLOWED but no docs matched")
        except OperationFailure as e:
            print(f"✅ Delete One: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # Test 12: Delete Many Documents
        try:
            result = db.customers.delete_many({"test_field": {"$exists": True}})
            if result.deleted_count > 0:
                print(f"❌ SECURITY ISSUE: Delete Many SUCCEEDED (deleted {result.deleted_count} docs)")
                print("   ⚠️  WARNING: User has DELETE permissions! Not read-only!")
            else:
                print(f"❌ SECURITY ISSUE: Delete Many ALLOWED but no docs matched")
        except OperationFailure as e:
            print(f"✅ Delete Many: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # =====================================================================
        # ADMINISTRATIVE OPERATIONS (Should Fail)
        # =====================================================================
        print("\n\n🚫 TESTING ADMINISTRATIVE OPERATIONS (Should Be Blocked)")
        print("-" * 70)
        
        # Test 13: Create Collection
        try:
            db.create_collection("test_new_collection")
            print(f"❌ SECURITY ISSUE: Create Collection SUCCEEDED")
            print("   ⚠️  WARNING: User has ADMIN permissions! Not read-only!")
            # Try to clean up
            try:
                db.drop_collection("test_new_collection")
            except:
                pass
        except OperationFailure as e:
            print(f"✅ Create Collection: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # Test 14: Drop Collection
        try:
            db.test_collection.drop()
            print(f"❌ SECURITY ISSUE: Drop Collection SUCCEEDED")
            print("   ⚠️  WARNING: User has DROP permissions! Not read-only!")
        except OperationFailure as e:
            print(f"✅ Drop Collection: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # Test 15: Create Index
        try:
            db.customers.create_index("test_index_field")
            print(f"❌ SECURITY ISSUE: Create Index SUCCEEDED")
            print("   ⚠️  WARNING: User has INDEX permissions! Not read-only!")
        except OperationFailure as e:
            print(f"✅ Create Index: BLOCKED (read-only working) - {e.details.get('errmsg', 'Permission denied')}")
            write_tests_blocked += 1
        
        # =====================================================================
        # SUMMARY
        # =====================================================================
        print("\n\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        total_read_tests = 5
        total_write_tests = 10
        
        print(f"\n✅ Read Operations Passed: {read_tests_passed}/{total_read_tests}")
        print(f"🚫 Write Operations Blocked: {write_tests_blocked}/{total_write_tests}")
        
        if read_tests_passed >= 3 and write_tests_blocked == total_write_tests:
            print("\n🎉 SUCCESS: Database is properly configured as READ-ONLY!")
            print("   ✅ User can read data")
            print("   ✅ User CANNOT insert data")
            print("   ✅ User CANNOT update data")
            print("   ✅ User CANNOT delete data")
            print("   ✅ User CANNOT perform admin operations")
            print("\n🔒 Security Status: SECURE ✓")
        elif write_tests_blocked < total_write_tests:
            print("\n⚠️  WARNING: Database is NOT read-only!")
            print(f"   ❌ {total_write_tests - write_tests_blocked} write operations were ALLOWED")
            print("   🔧 Action Required: Restrict user permissions in MongoDB Atlas")
            print("\n🔒 Security Status: INSECURE ✗")
        else:
            print("\n⚠️  PARTIAL: Some read operations failed")
            print("   🔧 Check user permissions in MongoDB Atlas")
        
        # Close connection
        client.close()
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Possible issues:")
        print("  - Check your username and password")
        print("  - Verify your IP address is whitelisted in MongoDB Atlas")
        print("  - Ensure the cluster is running")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_readonly_permissions()

