import faiss
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
from typing import List, Tuple, Dict, Any, Optional
import logging

class ModuleStore:
    """Faiss vector store for the module"""

    def __init__(self, dimension: int = 384):
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

class VectorStore:
    def __init__(self, dimension: int = 384, 
                 use_pgvector: bool = False,
                 host: str = "localhost",
                 port: int = 5432,
                 dbname: str = "rules",
                 user: str = "coc",
                 password: str = "coc_rule"):
        """Initialize a vector store with FAISS or PostgreSQL with pgvector.
        
        Args:
            dimension: Dimensionality of the embedding vectors
                      Default is 384 for sentence-transformers, was 1536 for OpenAI
            use_pgvector: Whether to use PostgreSQL with pgvector extension
            host: PostgreSQL host (only used if use_pgvector is True)
            port: PostgreSQL port (only used if use_pgvector is True)
            dbname: Database name (only used if use_pgvector is True)
            user: Database user (only used if use_pgvector is True)
            password: Database password (only used if use_pgvector is True)
        """
        self.dimension = dimension
        self.use_pgvector = use_pgvector
        
        if use_pgvector:
            self.connection_params = {
                "host": host,
                "port": port,
                "dbname": dbname,
                "user": user,
                "password": password
            }
            # Initialize connection to PostgreSQL
            self._initialize_db()
        else:
            # Use FAISS for local vector storage
            self.index = faiss.IndexFlatL2(dimension)
            self.texts = []
    
    def _initialize_db(self) -> None:
        """Initialize database with pgvector extension if using PostgreSQL."""
        if not self.use_pgvector:
            return
            
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                # Enable pgvector extension
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Create schema for storing document content
                cursor.execute("CREATE SCHEMA IF NOT EXISTS coc_rules;")
                
                conn.commit()
                logging.info("Initialized database connection to PostgreSQL with pgvector")
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
        finally:
            conn.close()
    
    def _get_connection(self):
        """Get a connection to the PostgreSQL database."""
        if not self.use_pgvector:
            raise ValueError("PostgreSQL connection requested but use_pgvector is False")
        return psycopg2.connect(**self.connection_params)
        
    def add_texts(self, texts: List[str], embeddings: np.ndarray, document_name: Optional[str] = None):
        """Add texts and their embeddings to the store.
        
        Args:
            texts: List of text strings to add
            embeddings: NumPy array of embeddings
            document_name: Name of document (required for pgvector)
        """
        if self.use_pgvector:
            if not document_name:
                raise ValueError("document_name is required when using pgvector")
            
            # Add to PostgreSQL
            self._add_to_pgvector(texts, embeddings, document_name)
        else:
            # Add to FAISS
            self.texts.extend(texts)
            self.index.add(embeddings)
    
    def _add_to_pgvector(self, texts: List[str], embeddings: np.ndarray, document_name: str):
        """Add texts and embeddings to PostgreSQL with pgvector.
        
        Args:
            texts: List of text strings
            embeddings: NumPy array of embeddings
            document_name: Name of document for table name
        """
        table_name = document_name.split('.')[0].lower().replace('-', '_')
        
        # Create table if it doesn't exist
        self._create_table(table_name)
        
        # Store embeddings in database
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                # Prepare data for batch insert
                data = []
                for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                    # Using 1 as placeholder for page since we don't have page info
                    data.append((1, i, text, embedding.tolist()))
                
                # Batch insert
                execute_values(
                    cursor,
                    f"""
                    INSERT INTO coc_rules.{table_name} 
                    (page, chunk_index, content, embedding) 
                    VALUES %s
                    """,
                    data,
                    template="(%s, %s, %s, %s)"
                )
                
                conn.commit()
                logging.info(f"Stored {len(texts)} chunks in table {table_name}")
        except Exception as e:
            logging.error(f"Error adding texts to pgvector: {e}")
        finally:
            conn.close()
    
    def _create_table(self, table_name: str):
        """Create a table for vector storage if it doesn't exist."""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                # Create table with vector support
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS coc_rules.{table_name} (
                        id SERIAL PRIMARY KEY,
                        page INTEGER,
                        chunk_index INTEGER,
                        content TEXT NOT NULL,
                        embedding VECTOR({self.dimension}) NOT NULL
                    );
                """)
                
                # Create vector index
                cursor.execute(f"""
                    CREATE INDEX IF NOT EXISTS {table_name}_embedding_idx 
                    ON coc_rules.{table_name} USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                """)
                
                conn.commit()
                logging.info(f"Created table coc_rules.{table_name}")
        except Exception as e:
            logging.error(f"Error creating table: {e}")
        finally:
            conn.close()
    
    def search(self, query_embedding: np.ndarray, k: int = 3, 
               document_name: Optional[str] = None) -> List[Tuple[str, float]]:
        """Search for similar texts.
        
        Args:
            query_embedding: Embedding of the query
            k: Number of results to return
            document_name: Name of document to search (for pgvector)
            
        Returns:
            List of (text, score) tuples
        """
        if self.use_pgvector:
            # Search in PostgreSQL
            return self._search_pgvector(query_embedding, k, document_name)
        else:
            # Search in FAISS
            distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.texts):  # Ensure index is valid
                    results.append((self.texts[idx], float(distances[0][i])))
            return results
    
    def _search_pgvector(self, query_embedding: np.ndarray, k: int = 3, 
                        document_name: Optional[str] = None) -> List[Tuple[str, float]]:
        """Search for similar texts in PostgreSQL.
        
        Args:
            query_embedding: Embedding of the query
            k: Number of results to return
            document_name: Name of document to search (if None, search all)
            
        Returns:
            List of (text, score) tuples
        """
        if document_name:
            # Search in specific document
            return self._search_document(document_name, query_embedding, k)
        else:
            # Search in all documents
            return self._search_all_documents(query_embedding, k)
    
    def _search_document(self, document_name: str, query_embedding: np.ndarray, 
                         limit: int = 5) -> List[Tuple[str, float, str]]:
        """Search for similar content in a specific document.
        
        Args:
            document_name: Name of the document to search
            query_embedding: Embedding of the query
            limit: Maximum number of results to return
            
        Returns:
            List of (text, score, document_name) tuples
        """
        table_name = document_name.split('.')[0].lower().replace('-', '_')
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT content, 1 - (embedding <=> %s) AS similarity
                    FROM coc_rules.{table_name}
                    ORDER BY similarity DESC
                    LIMIT %s
                """, (query_embedding.tolist(), limit))
                
                results = []
                for content, similarity in cursor.fetchall():
                    results.append((content, float(similarity), table_name))
                
                return results
        except Exception as e:
            logging.error(f"Error searching document: {e}")
            return []
        finally:
            conn.close()
    
    def _search_all_documents(self, query_embedding: np.ndarray, 
                             limit: int = 5) -> List[Tuple[str, float, str]]:
        """Search for similar content across all documents.
        
        Args:
            query_embedding: Embedding of the query
            limit: Maximum number of results to return
            
        Returns:
            List of (text, score, document_name) tuples
        """
        results = []
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                # Get all tables in our schema
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables
                    WHERE table_schema = 'coc_rules'
                """)
                
                tables = [row[0] for row in cursor.fetchall()]
                
                # Search each table
                for table in tables:
                    cursor.execute(f"""
                        SELECT content, 1 - (embedding <=> %s) AS similarity
                        FROM coc_rules.{table}
                        ORDER BY similarity DESC
                        LIMIT %s
                    """, (query_embedding.tolist(), limit))
                    
                    for content, similarity in cursor.fetchall():
                        # Include the document name (table name) in the results
                        results.append((content, float(similarity), table))
                
                # Sort by similarity across all tables
                results.sort(key=lambda x: x[1], reverse=True)
                # Return top k results
                return results[:limit]
        except Exception as e:
            logging.error(f"Error searching all documents: {e}")
            return []
        finally:
            conn.close()
            
    def get_available_documents(self) -> List[str]:
        """Get a list of available document tables in the database.
        
        Returns:
            List of document names
        """
        if not self.use_pgvector:
            return []
            
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables
                    WHERE table_schema = 'coc_rules'
                """)
                
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error getting available documents: {e}")
            return []
        finally:
            conn.close()
            
    def get_document_content(self, document_name: str) -> List[Dict[str, Any]]:
        """Get the full content of a document.
        
        Args:
            document_name: Name of the document to retrieve
            
        Returns:
            List of document chunks with their content
        """
        if not self.use_pgvector:
            return []
            
        table_name = document_name.split('.')[0].lower().replace('-', '_')
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT id, page, chunk_index, content
                    FROM coc_rules.{table_name}
                    ORDER BY page, chunk_index
                """)
                
                results = []
                for id, page, chunk_index, content in cursor.fetchall():
                    results.append({
                        "id": id,
                        "page": page,
                        "chunk_index": chunk_index,
                        "content": content
                    })
                
                return results
        except Exception as e:
            logging.error(f"Error retrieving document content for {document_name}: {e}")
            return []
        finally:
            conn.close() 