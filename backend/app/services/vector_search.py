from typing import Dict, List
import json

# Optional ChromaDB import
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except (ImportError, Exception) as e:
    CHROMADB_AVAILABLE = False
    chromadb = None
    Settings = None
    print(f"Warning: ChromaDB not available: {e}")


class VectorSearchService:
    """Service for vector similarity search using ChromaDB"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.collection_name = "cash_buyers"
        
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory="./chroma_db"
                ))
                self.collection = self._get_or_create_collection()
            except Exception as e:
                print(f"Warning: Could not initialize ChromaDB: {e}")
                self.client = None
                self.collection = None
    
    def _get_or_create_collection(self):
        """Get or create the cash buyers collection"""
        if not self.client:
            return None
        try:
            return self.client.get_collection(name=self.collection_name)
        except:
            return self.client.create_collection(name=self.collection_name)
    
    async def generate_embedding(self, buyer_data: Dict) -> List[float]:
        """Generate embedding vector for buyer data"""
        # In production, use a proper embedding model (e.g., sentence-transformers)
        # For now, create a simple feature vector
        
        # Combine text features
        text_features = f"{buyer_data.get('name', '')} {buyer_data.get('company_name', '')} {buyer_data.get('city', '')} {buyer_data.get('state', '')}"
        
        # Simple embedding (in production, use sentence-transformers or OpenAI embeddings)
        # This is a placeholder - replace with actual embedding model
        embedding = [hash(text_features) % 1000 / 1000.0 for _ in range(384)]  # 384-dim vector
        
        return embedding
    
    async def add_buyer(self, buyer_id: str, buyer_data: Dict, embedding: List[float]):
        """Add buyer to vector database"""
        if not self.collection:
            return  # Skip if ChromaDB not available
        
        metadata = {
            "name": buyer_data.get("name"),
            "city": buyer_data.get("city", ""),
            "state": buyer_data.get("state", ""),
            "preferred_types": json.dumps(buyer_data.get("preferred_property_types", [])),
            "price_min": str(buyer_data.get("price_range_min", 0)),
            "price_max": str(buyer_data.get("price_range_max", 0))
        }
        
        try:
            self.collection.add(
                ids=[str(buyer_id)],
                embeddings=[embedding],
                metadatas=[metadata]
            )
        except Exception as e:
            print(f"Warning: Could not add buyer to ChromaDB: {e}")
    
    async def search_similar_buyers(self, criteria: Dict, limit: int = 10) -> List[Dict]:
        """Search for similar cash buyers based on criteria"""
        if not self.collection:
            return []  # Return empty if ChromaDB not available
        
        try:
            # Generate query embedding
            query_embedding = await self.generate_embedding(criteria)
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )
            
            # Format results
            similar_buyers = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i, buyer_id in enumerate(results['ids'][0]):
                    similar_buyers.append({
                        "buyer_id": buyer_id,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            
            return similar_buyers
        except Exception as e:
            print(f"Warning: Could not search ChromaDB: {e}")
            return []

