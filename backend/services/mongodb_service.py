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
    
    # Ride Operations (Historical Data from CSV)
    
    async def get_historical_rides(
        self,
        limit: int = 20,
        skip: int = 0,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical ride data from CSV (rides collection)
        
        Args:
            limit: Maximum number of rides to return
            skip: Number of rides to skip
            filter_query: MongoDB filter query
            
        Returns:
            List of historical ride data dicts
        """
        try:
            query = filter_query or {}
            rides = list(self.db.rides.find(
                query,
                {"_id": 0}
            ).sort("timestamp", -1).skip(skip).limit(limit))
            
            return rides
        except Exception as e:
            logger.error(f"Error fetching historical rides: {e}")
            return []
    
    # Pricing Decision Operations (New AI-Generated Pricing)
    
    async def create_pricing_decision(self, pricing_data: Dict[str, Any]) -> str:
        """
        Create new pricing decision record in pricing_decisions collection
        
        Args:
            pricing_data: Pricing decision information
            
        Returns:
            Created pricing decision ID
        """
        try:
            pricing_data["timestamp"] = datetime.now()
            
            result = self.db.pricing_decisions.insert_one(pricing_data)
            logger.info(f"Pricing decision created: {pricing_data.get('ride_id')}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating pricing decision: {e}")
            raise
    
    async def get_pricing_decision(self, ride_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pricing decision by ride ID
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            Pricing decision dict or None if not found
        """
        try:
            decision = self.db.pricing_decisions.find_one(
                {"ride_id": ride_id},
                {"_id": 0}
            )
            return decision
        except Exception as e:
            logger.error(f"Error fetching pricing decision {ride_id}: {e}")
            return None
    
    async def create_ride(self, ride_data: Dict[str, Any]) -> str:
        """
        DEPRECATED: Use create_pricing_decision for new pricing
        
        This method kept for backward compatibility but now creates pricing decisions.
        
        Args:
            ride_data: Ride information including pricing
            
        Returns:
            Created ride ID
        """
        logger.warning("create_ride called - redirecting to create_pricing_decision")
        return await self.create_pricing_decision(ride_data)
    
    async def get_ride(self, ride_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pricing decision by ride ID (checks pricing_decisions collection)
        
        For backward compatibility, but now queries pricing_decisions.
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            Pricing decision dict or None if not found
        """
        return await self.get_pricing_decision(ride_id)
    
    async def get_customer_pricing_decisions(
        self,
        customer_id: str,
        limit: int = 10,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all pricing decisions for a customer
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of decisions to return
            skip: Number of decisions to skip
            
        Returns:
            List of pricing decision dicts
        """
        try:
            decisions = list(self.db.pricing_decisions.find(
                {"customer_id": customer_id},
                {"_id": 0}
            ).sort("timestamp", -1).skip(skip).limit(limit))
            
            return decisions
        except Exception as e:
            logger.error(f"Error fetching pricing decisions for customer {customer_id}: {e}")
            return []
    
    async def get_customer_rides(
        self,
        customer_id: str,
        limit: int = 10,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all rides for a customer (backward compatibility - returns pricing decisions)
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of rides to return
            skip: Number of rides to skip
            
        Returns:
            List of pricing decision dicts
        """
        return await self.get_customer_pricing_decisions(customer_id, limit, skip)
    
    async def get_rides(self, limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        """
        Get all pricing decisions with pagination
        
        Args:
            limit: Maximum number of decisions to return
            skip: Number of decisions to skip
            
        Returns:
            List of pricing decision dicts
        """
        try:
            decisions = list(self.db.pricing_decisions.find(
                {},
                {"_id": 0}
            ).sort("timestamp", -1).skip(skip).limit(limit))
            
            return decisions
        except Exception as e:
            logger.error(f"Error fetching pricing decisions: {e}")
            return []
    
    async def delete_ride(self, ride_id: str) -> bool:
        """
        Delete a pricing decision
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.db.pricing_decisions.delete_one({"ride_id": ride_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting pricing decision {ride_id}: {e}")
            return False
    
    # Statistics and Aggregations
    
    async def get_ride_statistics(self) -> Dict[str, Any]:
        """
        Get pricing statistics using aggregation from pricing_decisions collection
        
        Returns:
            Dict containing statistics (total pricing decisions, revenue, averages, etc.)
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_pricing_decisions": {"$sum": 1},
                        "total_revenue": {"$sum": "$calculated_price"},
                        "average_price": {"$avg": "$calculated_price"},
                        "average_base_price": {"$avg": "$base_price"},
                        "average_surge": {"$avg": "$surge_multiplier"},
                        "average_distance": {"$avg": "$distance_km"}
                    }
                }
            ]
            
            result = list(self.db.pricing_decisions.aggregate(pipeline))
            
            if result:
                stats = result[0]
                return {
                    "total_pricing_decisions": stats.get("total_pricing_decisions", 0),
                    "total_revenue": round(stats.get("total_revenue", 0), 2),
                    "average_price": round(stats.get("average_price", 0), 2),
                    "average_base_price": round(stats.get("average_base_price", 0), 2),
                    "average_surge_multiplier": round(stats.get("average_surge", 0), 2),
                    "average_distance": round(stats.get("average_distance", 0), 2)
                }
            
            return {
                "total_pricing_decisions": 0,
                "total_revenue": 0.0,
                "average_price": 0.0,
                "average_base_price": 0.0,
                "average_surge_multiplier": 0.0,
                "average_distance": 0.0
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {
                "total_pricing_decisions": 0,
                "total_revenue": 0.0,
                "average_price": 0.0,
                "average_base_price": 0.0,
                "average_surge_multiplier": 0.0,
                "average_distance": 0.0
            }
    
    async def get_pricing_history(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get pricing history for a customer from pricing_decisions collection
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of records
            
        Returns:
            List of pricing history records
        """
        try:
            decisions = list(self.db.pricing_decisions.find(
                {"customer_id": customer_id},
                {
                    "_id": 0,
                    "ride_id": 1,
                    "distance_km": 1,
                    "base_price": 1,
                    "surge_multiplier": 1,
                    "calculated_price": 1,
                    "timestamp": 1,
                    "applied": 1
                }
            ).sort("timestamp", -1).limit(limit))
            
            return decisions
        except Exception as e:
            logger.error(f"Error fetching pricing history: {e}")
            return []
    
    # Driver Operations
    
    async def get_driver(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """
        Get driver data by ID
        
        Args:
            driver_id: Driver identifier
            
        Returns:
            Driver data dict or None if not found
        """
        try:
            driver = self.db.drivers.find_one(
                {"driver_id": driver_id},
                {"_id": 0}
            )
            return driver
        except Exception as e:
            logger.error(f"Error fetching driver {driver_id}: {e}")
            return None
    
    async def get_drivers(
        self,
        limit: int = 20,
        skip: int = 0,
        filter_query: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all drivers with pagination
        
        Args:
            limit: Maximum number of drivers to return
            skip: Number of drivers to skip
            filter_query: MongoDB filter query (e.g., {"status": "Active"})
            
        Returns:
            List of driver data dicts
        """
        try:
            query = filter_query or {}
            drivers = list(self.db.drivers.find(
                query,
                {"_id": 0}
            ).sort("name", 1).skip(skip).limit(limit))
            
            return drivers
        except Exception as e:
            logger.error(f"Error fetching drivers: {e}")
            return []
    
    async def get_active_drivers(
        self,
        location: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get active drivers, optionally filtered by location
        
        Args:
            location: Filter by current location
            limit: Maximum number of drivers to return
            
        Returns:
            List of active driver data dicts
        """
        try:
            query = {"status": "Active"}
            if location:
                query["current_location"] = location
            
            drivers = list(self.db.drivers.find(
                query,
                {"_id": 0}
            ).sort("rating", -1).limit(limit))
            
            return drivers
        except Exception as e:
            logger.error(f"Error fetching active drivers: {e}")
            return []
    
    async def create_driver(self, driver_data: Dict[str, Any]) -> str:
        """
        Create new driver record
        
        Args:
            driver_data: Driver information
            
        Returns:
            Created driver ID
        """
        try:
            driver_data["joined_date"] = datetime.now()
            
            result = self.db.drivers.insert_one(driver_data)
            logger.info(f"Driver created: {driver_data['driver_id']}")
            return driver_data["driver_id"]
            
        except DuplicateKeyError:
            logger.warning(f"Driver already exists: {driver_data.get('driver_id')}")
            return driver_data.get('driver_id')
        except Exception as e:
            logger.error(f"Error creating driver: {e}")
            raise
    
    async def update_driver(self, driver_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update driver information
        
        Args:
            driver_id: Driver identifier
            update_data: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.db.drivers.update_one(
                {"driver_id": driver_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating driver {driver_id}: {e}")
            return False
    
    async def get_driver_statistics(self) -> Dict[str, Any]:
        """
        Get driver statistics using aggregation
        
        Returns:
            Dict containing driver statistics
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_drivers": {"$sum": 1},
                        "active_drivers": {
                            "$sum": {"$cond": [{"$eq": ["$status", "Active"]}, 1, 0]}
                        },
                        "total_rides_completed": {"$sum": "$total_rides_completed"},
                        "total_earnings": {"$sum": "$total_earnings"},
                        "average_rating": {"$avg": "$rating"},
                        "average_earnings": {"$avg": "$total_earnings"}
                    }
                }
            ]
            
            result = list(self.db.drivers.aggregate(pipeline))
            
            if result:
                stats = result[0]
                return {
                    "total_drivers": stats.get("total_drivers", 0),
                    "active_drivers": stats.get("active_drivers", 0),
                    "total_rides_completed": stats.get("total_rides_completed", 0),
                    "total_earnings": round(stats.get("total_earnings", 0), 2),
                    "average_rating": round(stats.get("average_rating", 0), 2),
                    "average_earnings_per_driver": round(stats.get("average_earnings", 0), 2)
                }
            
            return {
                "total_drivers": 0,
                "active_drivers": 0,
                "total_rides_completed": 0,
                "total_earnings": 0.0,
                "average_rating": 0.0,
                "average_earnings_per_driver": 0.0
            }
        except Exception as e:
            logger.error(f"Error calculating driver statistics: {e}")
            return {
                "total_drivers": 0,
                "active_drivers": 0,
                "total_rides_completed": 0,
                "total_earnings": 0.0,
                "average_rating": 0.0,
                "average_earnings_per_driver": 0.0
            }


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

