"""
MongoDB Service - Full Implementation

Handles all MongoDB database operations for HoneyGo application.

Implementation: Dec 2 - COMPLETE
Dependencies: pymongo
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

logger = logging.getLogger(__name__)


class MongoDBService:
    """
    Service class for MongoDB operations
    
    Handles:
    - Customer data CRUD
    - Ride data CRUD
    - Historical pricing queries
    - Aggregations and statistics
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize MongoDB service
        
        Args:
            connection_string: MongoDB connection URI
        """
        self.connection_string = connection_string
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connected = False
        logger.info("MongoDBService initialized")
    
    async def connect(self):
        """
        Establish connection to MongoDB
        
        Raises:
            ConnectionFailure: If connection to MongoDB fails
        """
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client["honeygo"]
            self.connected = True
            
            logger.info("✅ MongoDB connected successfully")
            
            # Create indexes
            await self._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.connected = False
            raise
    
    async def disconnect(self):
        """
        Close MongoDB connection
        """
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("MongoDB connection closed")
    
    async def _create_indexes(self):
        """
        Create database indexes for performance
        """
        try:
            # Rides indexes
            self.db.rides.create_index("ride_id", unique=True)
            self.db.rides.create_index("customer_id")
            self.db.rides.create_index("created_at")
            
            # Customers indexes
            self.db.customers.create_index("customer_id", unique=True)
            self.db.customers.create_index("loyalty_status")
            
            logger.info("✅ Database indexes created")
        except Exception as e:
            logger.warning(f"Index creation warning: {e}")
    
    # Customer Operations
    
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get customer data by ID
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Customer data dict or None if not found
        """
        try:
            customer = self.db.customers.find_one(
                {"customer_id": customer_id},
                {"_id": 0}  # Exclude MongoDB's _id field
            )
            return customer
        except Exception as e:
            logger.error(f"Error fetching customer {customer_id}: {e}")
            return None
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> str:
        """
        Create new customer record
        
        Args:
            customer_data: Customer information
            
        Returns:
            Created customer ID
        """
        try:
            customer_data["created_at"] = datetime.now()
            customer_data["updated_at"] = datetime.now()
            
            result = self.db.customers.insert_one(customer_data)
            logger.info(f"Customer created: {customer_data['customer_id']}")
            return customer_data["customer_id"]
            
        except DuplicateKeyError:
            logger.warning(f"Customer already exists: {customer_data.get('customer_id')}")
            return customer_data.get('customer_id')
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            raise
    
    async def update_customer(self, customer_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update customer information
        
        Args:
            customer_id: Customer identifier
            update_data: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            update_data["updated_at"] = datetime.now()
            
            result = self.db.customers.update_one(
                {"customer_id": customer_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {e}")
            return False
    
    # Ride Operations
    
    async def create_ride(self, ride_data: Dict[str, Any]) -> str:
        """
        Create new ride record
        
        Args:
            ride_data: Ride information including pricing
            
        Returns:
            Created ride ID
        """
        try:
            ride_data["created_at"] = datetime.now()
            
            result = self.db.rides.insert_one(ride_data)
            logger.info(f"Ride created: {ride_data['ride_id']}")
            return ride_data["ride_id"]
            
        except Exception as e:
            logger.error(f"Error creating ride: {e}")
            raise
    
    async def get_ride(self, ride_id: str) -> Optional[Dict[str, Any]]:
        """
        Get ride data by ID
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            Ride data dict or None if not found
        """
        try:
            ride = self.db.rides.find_one(
                {"ride_id": ride_id},
                {"_id": 0}
            )
            return ride
        except Exception as e:
            logger.error(f"Error fetching ride {ride_id}: {e}")
            return None
    
    async def get_customer_rides(
        self,
        customer_id: str,
        limit: int = 10,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all rides for a customer
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of rides to return
            skip: Number of rides to skip
            
        Returns:
            List of ride data dicts
        """
        try:
            rides = list(self.db.rides.find(
                {"customer_id": customer_id},
                {"_id": 0}
            ).sort("created_at", -1).skip(skip).limit(limit))
            
            return rides
        except Exception as e:
            logger.error(f"Error fetching rides for customer {customer_id}: {e}")
            return []
    
    async def get_rides(self, limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        """
        Get all rides with pagination
        
        Args:
            limit: Maximum number of rides to return
            skip: Number of rides to skip
            
        Returns:
            List of ride data dicts
        """
        try:
            rides = list(self.db.rides.find(
                {},
                {"_id": 0}
            ).sort("created_at", -1).skip(skip).limit(limit))
            
            return rides
        except Exception as e:
            logger.error(f"Error fetching rides: {e}")
            return []
    
    async def delete_ride(self, ride_id: str) -> bool:
        """
        Delete a ride
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.db.rides.delete_one({"ride_id": ride_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting ride {ride_id}: {e}")
            return False
    
    # Statistics and Aggregations
    
    async def get_ride_statistics(self) -> Dict[str, Any]:
        """
        Get ride statistics using aggregation
        
        Returns:
            Dict containing statistics (total rides, revenue, averages, etc.)
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_rides": {"$sum": 1},
                        "total_revenue": {"$sum": "$final_price"},
                        "average_price": {"$avg": "$final_price"},
                        "average_distance": {"$avg": "$distance_km"}
                    }
                }
            ]
            
            result = list(self.db.rides.aggregate(pipeline))
            
            if result:
                stats = result[0]
                return {
                    "total_rides": stats.get("total_rides", 0),
                    "total_revenue": round(stats.get("total_revenue", 0), 2),
                    "average_price": round(stats.get("average_price", 0), 2),
                    "average_distance": round(stats.get("average_distance", 0), 2)
                }
            
            return {
                "total_rides": 0,
                "total_revenue": 0.0,
                "average_price": 0.0,
                "average_distance": 0.0
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {
                "total_rides": 0,
                "total_revenue": 0.0,
                "average_price": 0.0,
                "average_distance": 0.0
            }
    
    async def get_pricing_history(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get pricing history for a customer
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of records
            
        Returns:
            List of pricing history records
        """
        try:
            rides = list(self.db.rides.find(
                {"customer_id": customer_id},
                {
                    "_id": 0,
                    "ride_id": 1,
                    "distance_km": 1,
                    "base_price": 1,
                    "surge_multiplier": 1,
                    "final_price": 1,
                    "created_at": 1
                }
            ).sort("created_at", -1).limit(limit))
            
            return rides
        except Exception as e:
            logger.error(f"Error fetching pricing history: {e}")
            return []


# Global instance (will be initialized in main.py startup event)
mongodb_service: Optional[MongoDBService] = None


def get_mongodb_service() -> MongoDBService:
    """
    Dependency injection function for FastAPI
    
    Returns:
        MongoDBService instance
    """
    if mongodb_service is None:
        raise RuntimeError("MongoDB service not initialized")
    return mongodb_service

