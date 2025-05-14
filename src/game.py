from typing import List, Dict
from .embeddings import EmbeddingManager
from .vector_store import VectorStore
from .llm import LLMManager

class CoCGame:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()
        self.llm_manager = LLMManager()
        self.conversation_history = []
        self.module_texts = []
        
    def load_module(self, module_texts: List[str]):
        """Load module texts into the vector store."""
        print("Loading module texts into the vector store...")
        embeddings = self.embedding_manager.get_embeddings(module_texts)
        print("Embedding module texts done.")
        print("Adding module texts to the vector store...")
        self.vector_store.add_texts(module_texts, embeddings)
        print("Adding module texts to the vector store done.")
        self.module_texts = module_texts
        
    def process_player_input(self, player_input: str) -> str:
        """Process player input and generate game master response."""
        # Get relevant context from vector store
        query_embedding = self.embedding_manager.get_embedding(player_input)
        relevant_texts = self.vector_store.search(query_embedding)
        context = "Environment Context:\n".join([text for text, _ in relevant_texts])
        
        # Add player input to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": player_input + "\n" + context
        })
        
        # Get response from LLM
        self.conversation_history,response = self.llm_manager.get_response(
            self.conversation_history,
            self.module_texts
        )
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        return response 