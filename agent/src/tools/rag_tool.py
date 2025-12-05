"""
RAG Tool for LangChain Agent

Provides semantic search and knowledge retrieval from ChromaDB.
"""

from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class RAGToolInput(BaseModel):
    """Input schema for RAG tool"""
    query: str = Field(description="The search query for semantic knowledge retrieval")
    collection: str = Field(
        default="hon_knowledge",
        description="Collection to search: 'hon_knowledge', 'pricing_reasoning', or 'similar_contexts'"
    )
    n_results: int = Field(
        default=3,
        description="Number of results to return (1-10)"
    )


class RAGTool(BaseTool):
    """
    Tool for retrieving relevant knowledge using RAG (Retrieval-Augmented Generation)
    
    Uses ChromaDB for semantic search across:
    - Honeywell domain knowledge
    - Historical pricing reasoning
    - Similar contextual situations
    """
    
    name: str = "semantic_knowledge_retrieval"
    description: str = """
    Retrieve relevant knowledge using semantic search.
    
    Use this tool when you need:
    - Honeywell domain knowledge and best practices
    - Similar historical pricing decisions and reasoning
    - Contextually similar situations from the past
    
    Input: A natural language query describing what you're looking for.
    Output: Relevant knowledge items with context and metadata.
    
    Examples:
    - "What is Honeywell's approach to surge pricing during weather events?"
    - "Find similar pricing decisions for urban evening rides with rain"
    - "What are best practices for customer loyalty discounts?"
    """
    args_schema: Type[BaseModel] = RAGToolInput
    chromadb_client: Optional[object] = None  # Will be injected
    
    def _run(self, query: str, collection: str = "hon_knowledge", n_results: int = 3) -> str:
        """
        Execute semantic search
        
        Args:
            query: Search query
            collection: Collection to search
            n_results: Number of results
            
        Returns:
            Formatted search results
        """
        try:
            if not self.chromadb_client:
                return "Error: ChromaDB client not available. RAG functionality disabled."
            
            # Validate collection
            valid_collections = ["hon_knowledge", "pricing_reasoning", "similar_contexts"]
            if collection not in valid_collections:
                collection = "hon_knowledge"
            
            # Clamp n_results
            n_results = max(1, min(10, n_results))
            
            # Query ChromaDB
            results = self.chromadb_client.query_knowledge(
                query=query,
                collection_name=collection,
                n_results=n_results
            )
            
            if not results:
                return f"No relevant knowledge found for: {query}"
            
            # Format results
            formatted = f"Found {len(results)} relevant knowledge items:\n\n"
            
            for i, result in enumerate(results, 1):
                text = result.get('text', 'No text available')
                metadata = result.get('metadata', {})
                distance = result.get('distance', 'N/A')
                
                formatted += f"[Result {i}]\n"
                formatted += f"Content: {text}\n"
                
                if metadata:
                    formatted += f"Metadata: "
                    formatted += ", ".join([f"{k}: {v}" for k, v in metadata.items()])
                    formatted += "\n"
                
                formatted += f"Relevance Score: {1 - distance if isinstance(distance, float) else 'N/A'}\n"
                formatted += "\n"
            
            logger.info(f"RAG tool returned {len(results)} results for query: {query[:50]}...")
            return formatted
            
        except Exception as e:
            logger.error(f"Error in RAG tool: {e}")
            return f"Error retrieving knowledge: {str(e)}"
    
    async def _arun(self, query: str, collection: str = "hon_knowledge", n_results: int = 3) -> str:
        """Async version (calls sync version for now)"""
        return self._run(query, collection, n_results)


def create_rag_tool(chromadb_client) -> RAGTool:
    """
    Factory function to create RAG tool with ChromaDB client
    
    Args:
        chromadb_client: ChromaDB client instance
        
    Returns:
        Configured RAG tool
    """
    tool = RAGTool()
    tool.chromadb_client = chromadb_client
    return tool

