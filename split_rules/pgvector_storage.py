import os
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import PyPDF2
from typing import List, Dict, Any, Tuple
import sys
from pathlib import Path

# Add src to path to import embeddings
sys.path.append(str(Path(__file__).parent.parent))
from src.embeddings import EmbeddingManager

class PGVectorStorage:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "rules",
        user: str = "coc",
        password: str = "coc_rule",
        embedding_model: str = "all-mpnet-base-v2",
        chunk_size: int = 500
    ):
        """Initialize connection to PostgreSQL with pgvector extension.
        
        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            dbname: Database name
            user: Database user
            password: Database password
            embedding_model: Model name for sentence embeddings
            chunk_size: Number of characters per text chunk
        """
        self.connection_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password
        }
        self.chunk_size = chunk_size
        self.embedding_manager = EmbeddingManager(model_name=embedding_model)
        self.vector_dim = self.embedding_manager.dimension
        
        # Initialize database
        self._initialize_db()
    
    def _initialize_db(self) -> None:
        """Initialize database with pgvector extension and create schema if needed."""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                # Enable pgvector extension
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Create schema for storing document content
                cursor.execute("""
                    CREATE SCHEMA IF NOT EXISTS coc_rules;
                """)
                
                conn.commit()
        finally:
            conn.close()

    def _get_connection(self):
        """Get a connection to the PostgreSQL database."""
        return psycopg2.connect(**self.connection_params)
    
    def create_table_for_document(self, document_name: str) -> None:
        """Create a table for a specific document if it doesn't exist.
        
        Args:
            document_name: Name of the document (will be used as table name)
        """
        # Sanitize table name (remove extension and invalid chars)
        table_name = document_name.split('.')[0].lower().replace('-', '_')
        
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
                        embedding VECTOR({self.vector_dim}) NOT NULL
                    );
                """)
                
                # Create vector index
                cursor.execute(f"""
                    CREATE INDEX IF NOT EXISTS {table_name}_embedding_idx 
                    ON coc_rules.{table_name} USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                """)
                
                conn.commit()
                print(f"Created table coc_rules.{table_name}")
        finally:
            conn.close()
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Tuple[int, str]]:
        """Extract text from PDF file with page numbers.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of (page_number, text) tuples
        """
        result = []
        
        try:
            reader = PyPDF2.PdfReader(pdf_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    result.append((i+1, text))
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
        
        return result
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks of approximately chunk_size characters.
        
        Args:
            text: Text to split into chunks
            
        Returns:
            List of text chunks
        """
        # Simple chunking by character count
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                # Add current chunk if it's not empty
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk
                if len(paragraph) <= self.chunk_size:
                    current_chunk = paragraph + "\n\n"
                else:
                    # Split long paragraphs
                    words = paragraph.split()
                    current_chunk = ""
                    for word in words:
                        if len(current_chunk) + len(word) + 1 <= self.chunk_size:
                            current_chunk += word + " "
                        else:
                            chunks.append(current_chunk.strip())
                            current_chunk = word + " "
                    
                    if current_chunk:
                        current_chunk += "\n\n"
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def store_document(self, pdf_path: str) -> None:
        """Process and store a document in the vector database.
        
        Args:
            pdf_path: Path to the PDF file
        """
        document_name = os.path.basename(pdf_path)
        table_name = document_name.split('.')[0].lower().replace('-', '_')
        
        # Create table for the document
        self.create_table_for_document(document_name)
        
        # Extract text from PDF
        page_texts = self.extract_text_from_pdf(pdf_path)
        
        # Process each page
        for page_num, text in page_texts:
            # Chunk the text
            chunks = self.chunk_text(text)
            
            # Create embeddings for chunks
            if chunks:
                embeddings = self.embedding_manager.get_embeddings(chunks)
                
                # Store in database
                conn = self._get_connection()
                try:
                    with conn.cursor() as cursor:
                        # Prepare data for batch insert
                        data = []
                        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                            data.append((page_num, i, chunk, embedding.tolist()))
                        
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
                    print(f"Stored {len(chunks)} chunks from page {page_num} of {document_name}")
                finally:
                    conn.close()
    
    def search_document(self, document_name: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content in a specific document.
        
        Args:
            document_name: Name of the document to search
            query: Query text
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries with page, content, and similarity score
        """
        table_name = document_name.split('.')[0].lower().replace('-', '_')
        query_embedding = self.embedding_manager.get_embedding(query)
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT page, content, 1 - (embedding <=> %s) AS similarity
                    FROM coc_rules.{table_name}
                    ORDER BY similarity DESC
                    LIMIT %s
                """, (query_embedding.tolist(), limit))
                
                results = []
                for page, content, similarity in cursor.fetchall():
                    results.append({
                        "page": page,
                        "content": content,
                        "similarity": similarity
                    })
                
                return results
        finally:
            conn.close()
    
    def search_all_documents(self, query: str, limit: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Search for similar content across all documents.
        
        Args:
            query: Query text
            limit: Maximum number of results to return per document
            
        Returns:
            Dictionary mapping document names to lists of results
        """
        query_embedding = self.embedding_manager.get_embedding(query)
        results = {}
        
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
                        SELECT page, content, 1 - (embedding <=> %s) AS similarity
                        FROM coc_rules.{table}
                        ORDER BY similarity DESC
                        LIMIT %s
                    """, (query_embedding.tolist(), limit))
                    
                    doc_results = []
                    for page, content, similarity in cursor.fetchall():
                        doc_results.append({
                            "page": page,
                            "content": content,
                            "similarity": similarity
                        })
                    
                    if doc_results:
                        # Convert snake_case back to original filename
                        doc_name = f"{table}.pdf"
                        results[doc_name] = doc_results
                
                return results
        finally:
            conn.close()


def process_all_pdfs(directory: str):
    """Process all PDF files in a directory and store them in pgvector.
    
    Args:
        directory: Path to the directory containing PDF files
    """
    storage = PGVectorStorage()
    
    # Process all PDF files
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            print(f"Processing {filename}...")
            storage.store_document(pdf_path)


if __name__ == "__main__":
    # Get the directory from the first argument or use the current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)
    process_all_pdfs(directory)
