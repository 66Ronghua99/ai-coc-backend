from typing import List, Dict
from .embeddings import EmbeddingManager
from .vector_store import VectorStore
from .llm import LLMManager

class CoCGame:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.module = VectorStore(dimension=self.embedding_manager.dimension)
        self.rules = VectorStore(dimension=self.embedding_manager.dimension)
        self.llm_manager = LLMManager()
        self.conversation_history = []

    def load_rules(self, rules_texts: List[str]):
        """Load rules texts into the vector store."""
        print("Loading rules texts into the vector store...")
        embeddings = self.embedding_manager.get_embeddings(rules_texts)
        print("Embedding rules texts done.")
        print("Adding rules texts to the vector store...")
        self.rules.add_texts(rules_texts, embeddings)
        print("Adding rules texts to the vector store done.")
        self.rules_texts = rules_texts

    def load_module(self, module_texts: List[str]):
        """Load module texts into the vector store."""
        print("Loading module texts into the vector store...")
        embeddings = self.embedding_manager.get_embeddings(module_texts)
        print("Embedding module texts done.")
        print("Adding module texts to the vector store...")
        self.module.add_texts(module_texts, embeddings)
        print("Adding module texts to the vector store done.")
        self.llm_manager.load_scenario(str(module_texts))
        
    def process_player_input(self, player_input: str) -> str:
        """Process player input and generate game master response."""
        # Get relevant context from vector store
        query_embedding = self.embedding_manager.get_embedding(player_input)
        relevant_texts = self.module.search(query_embedding)
        module_context = "\n".join([text for text, _ in relevant_texts])
        rules_context = "\n".join([text for text, _ in self.rules.search(query_embedding)])
        
        # Get response from LLM
        self.conversation_history,response = self.llm_manager.get_response(
            self.conversation_history,
            player_input,
            module_context,
            rules_context
        )
        if not response:
            response = "<发生了一些错误，请重新尝试/>"
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        return response 