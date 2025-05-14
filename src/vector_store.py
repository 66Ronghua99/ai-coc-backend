import faiss
import numpy as np
from typing import List, Tuple

class VectorStore:
    def __init__(self, dimension: int = 384):
        """Initialize a vector store with FAISS.
        
        Args:
            dimension: Dimensionality of the embedding vectors
                      Default is 384 for sentence-transformers, was 1536 for OpenAI
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
        
    def add_texts(self, texts: List[str], embeddings: np.ndarray):
        """Add texts and their embeddings to the store."""
        self.texts.extend(texts)
        self.index.add(embeddings)
        
    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Tuple[str, float]]:
        """Search for similar texts."""
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):  # Ensure index is valid
                results.append((self.texts[idx], float(distances[0][i])))
        return results 