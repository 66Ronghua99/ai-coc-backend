import numpy as np
from typing import List, Dict, Any, Optional
import logging
from .vector_store import VectorStore
from .embeddings import EmbeddingManager

class VectorManager:
    """Manager class to handle vector store operations and function calls."""
    
    def __init__(
        self,
        use_pgvector: bool = True,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "rules",
        user: str = "coc",
        password: str = "coc_rule",
        embedding_model: str = "all-mpnet-base-v2"
    ):
        """Initialize the vector manager.
        
        Args:
            use_pgvector: Whether to use PostgreSQL with pgvector
            host: PostgreSQL host
            port: PostgreSQL port
            dbname: Database name
            user: Database user
            password: Database password
            embedding_model: Model name for embeddings
        """
        self.embedding_manager = EmbeddingManager(model_name=embedding_model)
        self.vector_store = VectorStore(
            dimension=self.embedding_manager.dimension,
            use_pgvector=use_pgvector,
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def search_all_rules(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search all rule documents for relevant information.
        
        Args:
            query: The query text
            limit: Maximum number of results to return
            
        Returns:
            Dictionary with results
        """
        try:
            # Get the embedding for the query
            query_embedding = self.embedding_manager.get_embedding(query)
            
            # Search across all documents
            results = self.vector_store._search_all_documents(query_embedding, limit)
            
            # Format the results
            formatted_results = []
            for text, score, document_name in results:
                formatted_results.append({
                    "content": text,
                    "document": document_name,
                    "relevance_score": round(score, 3)
                })
            
            return {
                "query": query,
                "results": formatted_results
            }
        except Exception as e:
            self.logger.error(f"Error searching all rules: {e}")
            return {
                "query": query,
                "error": str(e),
                "results": []
            }
    
    def search_document(self, document_name: str, query: str, limit: int = 3) -> Dict[str, Any]:
        """Search a specific document for relevant information.
        
        Args:
            document_name: Name of the document to search
            query: The query text
            limit: Maximum number of results to return
            
        Returns:
            Dictionary with results
        """
        try:
            # Get the embedding for the query
            query_embedding = self.embedding_manager.get_embedding(query)
            
            # Search in the specific document
            results = self.vector_store._search_document(document_name, query_embedding, limit)
            
            # Format the results
            formatted_results = []
            for text, score, doc_name in results:
                formatted_results.append({
                    "content": text,
                    "document": doc_name,
                    "relevance_score": round(score, 3)
                })
            
            return {
                "query": query,
                "document": document_name,
                "results": formatted_results
            }
        except Exception as e:
            self.logger.error(f"Error searching document {document_name}: {e}")
            return {
                "query": query,
                "document": document_name,
                "error": str(e),
                "results": []
            }
    
    def get_available_rule_documents(self) -> Dict[str, Any]:
        """Get a list of available rule documents.
        
        Returns:
            Dictionary with document names
        """
        try:
            documents = self.vector_store.get_available_documents()
            return {
                "documents": documents
            }
        except Exception as e:
            self.logger.error(f"Error getting available documents: {e}")
            return {
                "error": str(e),
                "documents": []
            }
    
    def function_calling(self, function_name: str, parameters: Dict[str, Any]) -> Any:
        """Handle function calls for vector search operations.
        
        Args:
            function_name: Name of the function to call
            parameters: Function parameters
            
        Returns:
            Function result
        """
        if function_name == "search_all_rules":
            limit = parameters.get("limit", 5)
            return self.search_all_rules(parameters["query"], limit)
        
        elif function_name == "get_available_rule_documents":
            return self.get_available_rule_documents()
        
        elif function_name in [
            "retrieve_coc_rules_skills", 
            "retrieve_coc_rules_sanity", 
            "retrieve_coc_mythos_creatures_gods", 
            "retrieve_coc_rules_keeper_guide", 
            "retrieve_coc_rules_game_system", 
            "retrieve_coc_rules_chase", 
            "retrieve_coc_rules_combat", 
            "retrieve_coc_rules_alien_technology", 
            "retrieve_coc_rules_investigator_creation"
        ]:
            # Extract the document name from the function name
            document_name = function_name.replace("retrieve_coc_rules_", "")
            query = parameters.get("query", "")
            limit = parameters.get("limit", 5)
            
            # If query is provided, search the specific document
            if query:
                return self.search_document(document_name, query, limit)
            # Otherwise, return the whole document content
            else:
                try:
                    document_content = self.vector_store.get_document_content(document_name)
                    return {
                        "document": document_name,
                        "content": document_content
                    }
                except Exception as e:
                    self.logger.error(f"Error retrieving document {document_name}: {e}")
                    return {
                        "document": document_name,
                        "error": str(e),
                        "content": []
                    }
        else:
            raise ValueError(f"Unknown function: {function_name}") 