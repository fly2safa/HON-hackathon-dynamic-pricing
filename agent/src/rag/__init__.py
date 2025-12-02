"""
RAG (Retrieval-Augmented Generation) Module

Provides ChromaDB integration for semantic search and knowledge retrieval.
"""

from .chromadb_client import ChromaDBClient
from .knowledge_base import seed_hon_knowledge, seed_pricing_reasoning

__all__ = [
    'ChromaDBClient',
    'seed_hon_knowledge',
    'seed_pricing_reasoning'
]

