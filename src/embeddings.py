import os
from typing import List
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EmbeddingManager:
    def __init__(self):
        """Initialize the embedding manager with OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return np.array(response.data[0].embedding)
        
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings for multiple texts."""
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        return np.array(embeddings) 