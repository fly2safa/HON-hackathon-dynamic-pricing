"""
ChromaDB Service

Handles vector database operations for RAG (Retrieval-Augmented Generation).
Uses ChromaDB for semantic search over historical pricing decisions and HON knowledge.

Dependencies: chromadb
"""

from typing import Optional, List, Dict, Any
import logging
import os
import chromadb
from chromadb.config import Settings
import uuid

logger = logging.getLogger(__name__)


class ChromaDBService:
    """
    Service class for ChromaDB vector database operations
    
    Handles:
    - HON domain knowledge retrieval
    - Historical pricing reasoning retrieval
    - Semantic search for relevant context
    """
    
    def __init__(
        self,
        persist_directory: str = "./chromadb_data"
    ):
        """
        Initialize ChromaDB service with persistent local storage
        
        Args:
            persist_directory: Directory for persistent storage
        """
        self.persist_directory = persist_directory
        self.client = None
        self.collections = {}
        self.connected = False
        
        logger.info(f"ChromaDBService initialized (persist_dir: {persist_directory})")
    
    async def connect(self):
        """
        Establish connection to ChromaDB (local persistent mode)
        """
        try:
            # Ensure directory exists
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Initialize persistent client
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collections
            self.collections["pricing_decisions"] = self.client.get_or_create_collection(
                name="pricing_decisions",
                metadata={"description": "Historical pricing decisions with reasoning"}
            )
            
            self.collections["rides"] = self.client.get_or_create_collection(
                name="rides", 
                metadata={"description": "Historical ride data for similarity search"}
            )
            
            self.connected = True
            
            # Log collection stats
            pricing_count = self.collections["pricing_decisions"].count()
            rides_count = self.collections["rides"].count()
            
            logger.info(f"✅ ChromaDB connected - Collections: pricing_decisions({pricing_count}), rides({rides_count})")
            
        except Exception as e:
            logger.error(f"❌ ChromaDB connection failed: {e}")
            self.connected = False
            raise
    
    async def disconnect(self):
        """
        Close ChromaDB connection
        """
        self.client = None
        self.collections = {}
        self.connected = False
        logger.info("ChromaDB connection closed")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        if not self.connected:
            return {"connected": False}
        
        return {
            "connected": True,
            "persist_directory": self.persist_directory,
            "collections": {
                name: coll.count() for name, coll in self.collections.items()
            }
        }
    
    async def query_similar_rides(
        self,
        query: str,
        n_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query for similar rides using semantic search
        
        Args:
            query: Search query (e.g., "Urban Premium ride at Night")
            n_results: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of similar rides with scores
        """
        if not self.connected or "rides" not in self.collections:
            logger.warning("ChromaDB not connected for ride query")
            return []
        
        try:
            collection = self.collections["rides"]
            
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filters if filters else None
            )
            
            # Format results
            formatted = []
            if results and results['ids'] and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    formatted.append({
                        "id": doc_id,
                        "text": results['documents'][0][i] if results['documents'] else "",
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0,
                        "similarity": 1 - (results['distances'][0][i] if results['distances'] else 0)
                    })
            
            logger.info(f"🔍 ChromaDB query: '{query[:50]}...' → {len(formatted)} results")
            return formatted
            
        except Exception as e:
            logger.error(f"ChromaDB query error: {e}")
            return []
    
    async def query_pricing_decisions(
        self,
        scenario: str,
        n_results: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get similar historical pricing decisions for RAG
        
        Args:
            scenario: Current pricing scenario description
            n_results: Number of similar cases to retrieve
            
        Returns:
            List of similar pricing decisions with reasoning
        """
        if not self.connected or "pricing_decisions" not in self.collections:
            logger.warning("ChromaDB not connected for pricing query")
            return []
        
        try:
            collection = self.collections["pricing_decisions"]
            
            results = collection.query(
                query_texts=[scenario],
                n_results=n_results
            )
            
            # Format results
            formatted = []
            if results and results['ids'] and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    formatted.append({
                        "id": doc_id,
                        "reasoning": results['documents'][0][i] if results['documents'] else "",
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "similarity": 1 - (results['distances'][0][i] if results['distances'] else 0)
                    })
            
            logger.info(f"🎯 ChromaDB pricing query: '{scenario[:50]}...' → {len(formatted)} similar decisions")
            return formatted
            
        except Exception as e:
            logger.error(f"ChromaDB pricing query error: {e}")
            return []
    
    async def add_ride(
        self,
        ride_text: str,
        metadata: Dict[str, Any],
        ride_id: Optional[str] = None
    ) -> str:
        """
        Add a ride to the vector database
        
        Args:
            ride_text: Text description of the ride
            metadata: Ride metadata (location, time, vehicle, price, etc.)
            ride_id: Optional ride ID (generated if not provided)
            
        Returns:
            Ride ID
        """
        if not self.connected or "rides" not in self.collections:
            raise RuntimeError("ChromaDB not connected")
        
        doc_id = ride_id or f"ride-{uuid.uuid4().hex[:8]}"
        
        try:
            self.collections["rides"].add(
                documents=[ride_text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.info(f"✅ Added ride to ChromaDB: {doc_id}")
            return doc_id
        except Exception as e:
            # Handle duplicate ID
            if "already exists" in str(e).lower():
                logger.warning(f"Ride {doc_id} already exists in ChromaDB")
                return doc_id
            raise
    
    async def add_pricing_decision(
        self,
        decision_text: str,
        metadata: Dict[str, Any],
        decision_id: Optional[str] = None
    ) -> str:
        """
        Store a pricing decision for future RAG retrieval
        
        Args:
            decision_text: The pricing decision and reasoning
            metadata: Context metadata (ride details, factors, etc.)
            decision_id: Optional ID (generated if not provided)
            
        Returns:
            Decision ID
        """
        if not self.connected or "pricing_decisions" not in self.collections:
            raise RuntimeError("ChromaDB not connected")
        
        doc_id = decision_id or f"decision-{uuid.uuid4().hex[:8]}"
        
        try:
            self.collections["pricing_decisions"].add(
                documents=[decision_text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.info(f"✅ Added pricing decision to ChromaDB: {doc_id}")
            return doc_id
        except Exception as e:
            if "already exists" in str(e).lower():
                logger.warning(f"Decision {doc_id} already exists in ChromaDB")
                return doc_id
            raise
    
    async def add_rides_batch(
        self,
        rides: List[Dict[str, Any]]
    ) -> int:
        """
        Add multiple rides in batch (for seeding)
        
        Args:
            rides: List of ride dictionaries
            
        Returns:
            Number of rides added
        """
        if not self.connected or "rides" not in self.collections:
            raise RuntimeError("ChromaDB not connected")
        
        documents = []
        metadatas = []
        ids = []
        
        for i, ride in enumerate(rides):
            # Create text description for embedding
            text = f"{ride.get('location_category', 'Unknown')} {ride.get('vehicle_type', 'Standard')} ride at {ride.get('time_of_booking', 'Unknown')} time. "
            text += f"Customer: {ride.get('customer_loyalty_status', 'Regular')}. "
            text += f"Duration: {ride.get('expected_ride_duration', 0)} mins. "
            text += f"Price: ${ride.get('historical_cost_of_ride', 0):.2f}"
            
            documents.append(text)
            metadatas.append({
                "location_category": str(ride.get('location_category', '')),
                "vehicle_type": str(ride.get('vehicle_type', '')),
                "time_of_booking": str(ride.get('time_of_booking', '')),
                "customer_loyalty_status": str(ride.get('customer_loyalty_status', '')),
                "expected_ride_duration": float(ride.get('expected_ride_duration', 0)),
                "historical_cost_of_ride": float(ride.get('historical_cost_of_ride', 0)),
                "number_of_riders": int(ride.get('number_of_riders', 0)),
                "number_of_drivers": int(ride.get('number_of_drivers', 0)),
                "average_ratings": float(ride.get('average_ratings', 0))
            })
            ids.append(f"ride-{i:05d}")
        
        try:
            # Add in batches of 100
            batch_size = 100
            added = 0
            
            for start in range(0, len(documents), batch_size):
                end = min(start + batch_size, len(documents))
                self.collections["rides"].add(
                    documents=documents[start:end],
                    metadatas=metadatas[start:end],
                    ids=ids[start:end]
                )
                added += (end - start)
                logger.info(f"📦 Added batch {start//batch_size + 1}: {added}/{len(documents)} rides")
            
            logger.info(f"✅ ChromaDB seeded with {added} rides")
            return added
            
        except Exception as e:
            logger.error(f"Batch add error: {e}")
            raise


# Global instance
chromadb_service: Optional[ChromaDBService] = None


def get_chromadb_service() -> Optional[ChromaDBService]:
    """
    Get ChromaDB service instance
    
    Returns:
        ChromaDBService instance or None if not initialized
    """
    return chromadb_service


async def init_chromadb_service(persist_directory: str = "./chromadb_data") -> ChromaDBService:
    """
    Initialize and connect ChromaDB service
    
    Args:
        persist_directory: Directory for persistent storage
        
    Returns:
        Connected ChromaDBService instance
    """
    global chromadb_service
    chromadb_service = ChromaDBService(persist_directory=persist_directory)
    await chromadb_service.connect()
    return chromadb_service

