import os
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        """Initialize the embedding manager with a local Hugging Face model.
        
        Args:
            model_name: Name of the sentence-transformers model to use
                       Default is 'all-mpnet-base-v2', a high-quality 768-dim model
                       Other options:
                       - 'all-MiniLM-L6-v2': Lightweight 384-dim (faster)
                       - 'multi-qa-mpnet-base-dot-v1': 768-dim optimized for retrieval
                       - 'e5-large-v2': High performance 1024-dim (slower)
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text."""
        return self.model.encode(text, convert_to_numpy=True)
        
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings for multiple texts efficiently in a batch."""
        return self.model.encode(texts, convert_to_numpy=True) 