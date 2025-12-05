"""
ChromaDB Client for RAG (Retrieval-Augmented Generation)

Handles vector database operations for the LangChain agent.
"""

from typing import List, Dict, Any, Optional
import logging
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import uuid
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class ChromaDBClient:
    """
    Client for ChromaDB vector database operations
    
    Provides semantic search and knowledge retrieval for the AI agent.
    """
    
    def __init__(
        self,
        persist_directory: str = "./chromadb_data",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize ChromaDB client
        
        Args:
            persist_directory: Directory for persistent storage
            embedding_model: Sentence transformer model for embeddings
        """
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.client = None
        self.collections = {}
        self.embedding_function = None
        
        logger.info(f"ChromaDBClient initialized with persist_directory={persist_directory}")
    
    def connect(self):
        """
        Establish connection to ChromaDB and initialize collections
        """
        try:
            # Create persist directory if it doesn't exist
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Initialize persistent client
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Initialize embedding function
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.embedding_model
            )
            
            # Get or create collections
            self.collections["hon_knowledge"] = self.client.get_or_create_collection(
                name="hon_knowledge",
                embedding_function=self.embedding_function,
                metadata={"description": "Honeywell domain knowledge and best practices"}
            )
            
            self.collections["pricing_reasoning"] = self.client.get_or_create_collection(
                name="pricing_reasoning",
                embedding_function=self.embedding_function,
                metadata={"description": "Historical pricing decisions and reasoning"}
            )
            
            self.collections["similar_contexts"] = self.client.get_or_create_collection(
                name="similar_contexts",
                embedding_function=self.embedding_function,
                metadata={"description": "Semantic search for contextually similar situations"}
            )
            
            logger.info("ChromaDB connected successfully with 3 collections")
            logger.info(f"  - hon_knowledge: {self.collections['hon_knowledge'].count()} documents")
            logger.info(f"  - pricing_reasoning: {self.collections['pricing_reasoning'].count()} documents")
            logger.info(f"  - similar_contexts: {self.collections['similar_contexts'].count()} documents")
            
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            raise
    
    def disconnect(self):
        """
        Close ChromaDB connection
        """
        try:
            if self.client:
                # ChromaDB persistent client doesn't need explicit disconnect
                # but we'll clear references
                self.collections.clear()
                self.client = None
                logger.info("ChromaDB disconnected successfully")
        except Exception as e:
            logger.error(f"Error during ChromaDB disconnection: {e}")
    
    def query_knowledge(
        self,
        query: str,
        collection_name: str = "hon_knowledge",
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query knowledge base using semantic search
        
        Args:
            query: Search query text
            collection_name: ChromaDB collection to query
            n_results: Number of results to return
            
        Returns:
            List of relevant knowledge items with similarity scores
        """
        try:
            if not self.client or collection_name not in self.collections:
                logger.error(f"Collection {collection_name} not available")
                return []
            
            collection = self.collections[collection_name]
            
            # Perform semantic search
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results and results['documents'] and len(results['documents']) > 0:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'id': results['ids'][0][i] if results['ids'] else None
                    })
            
            logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            return []
    
    def get_pricing_reasoning(
        self,
        scenario: str,
        n_results: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get similar historical pricing reasoning
        
        Args:
            scenario: Current pricing scenario description
            n_results: Number of similar cases to retrieve
            
        Returns:
            List of similar pricing decisions with reasoning
        """
        logger.info(f"Fetching pricing reasoning for scenario: {scenario[:50]}...")
        return self.query_knowledge(
            query=scenario,
            collection_name="pricing_reasoning",
            n_results=n_results
        )
    
    def add_knowledge(
        self,
        text: str,
        metadata: Dict[str, Any],
        collection_name: str = "hon_knowledge"
    ) -> str:
        """
        Add new knowledge item to the database
        
        Args:
            text: Knowledge text content
            metadata: Associated metadata
            collection_name: Target collection
            
        Returns:
            Item ID
        """
        try:
            if not self.client or collection_name not in self.collections:
                raise ValueError(f"Collection {collection_name} not available")
            
            collection = self.collections[collection_name]
            
            # Generate unique ID
            item_id = str(uuid.uuid4())
            
            # Add timestamp to metadata
            metadata['created_at'] = datetime.utcnow().isoformat()
            
            # Add to collection
            collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[item_id]
            )
            
            logger.info(f"Added knowledge item {item_id} to {collection_name}")
            return item_id
            
        except Exception as e:
            logger.error(f"Error adding knowledge item: {e}")
            raise
    
    def add_pricing_decision(
        self,
        decision_text: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Store a pricing decision for future RAG retrieval
        
        Args:
            decision_text: The pricing decision and reasoning
            metadata: Context metadata (ride details, factors, etc.)
            
        Returns:
            Decision ID
        """
        logger.info("Storing pricing decision")
        return self.add_knowledge(
            text=decision_text,
            metadata=metadata,
            collection_name="pricing_reasoning"
        )
    
    def add_bulk_knowledge(
        self,
        items: List[Dict[str, Any]],
        collection_name: str = "hon_knowledge"
    ) -> List[str]:
        """
        Add multiple knowledge items at once
        
        Args:
            items: List of dicts with 'text' and 'metadata' keys
            collection_name: Target collection
            
        Returns:
            List of item IDs
        """
        try:
            if not self.client or collection_name not in self.collections:
                raise ValueError(f"Collection {collection_name} not available")
            
            collection = self.collections[collection_name]
            
            # Prepare data
            ids = [str(uuid.uuid4()) for _ in items]
            documents = [item['text'] for item in items]
            metadatas = []
            
            for item in items:
                metadata = item.get('metadata', {})
                metadata['created_at'] = datetime.utcnow().isoformat()
                metadatas.append(metadata)
            
            # Bulk add
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(ids)} knowledge items to {collection_name}")
            return ids
            
        except Exception as e:
            logger.error(f"Error adding bulk knowledge: {e}")
            raise
    
    def clear_collection(self, collection_name: str):
        """
        Clear all documents from a collection
        
        Args:
            collection_name: Collection to clear
        """
        try:
            if collection_name in self.collections:
                # Delete and recreate collection
                self.client.delete_collection(name=collection_name)
                self.collections[collection_name] = self.client.get_or_create_collection(
                    name=collection_name,
                    embedding_function=self.embedding_function
                )
                logger.info(f"Cleared collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error clearing collection {collection_name}: {e}")
            raise
    
    def get_collection_count(self, collection_name: str) -> int:
        """
        Get document count for a collection
        
        Args:
            collection_name: Collection name
            
        Returns:
            Number of documents
        """
        try:
            if collection_name in self.collections:
                return self.collections[collection_name].count()
            return 0
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0

