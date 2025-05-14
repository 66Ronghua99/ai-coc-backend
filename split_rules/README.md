# Call of Cthulhu Rules - pgVector Storage

This module provides a solution for storing and retrieving Call of Cthulhu rulebook content using PostgreSQL with the pgvector extension for vector similarity search.

## Requirements

- PostgreSQL 12+ with pgvector extension installed
- Python 3.8+
- Required Python packages:
  - psycopg2
  - numpy
  - pypdf
  - sentence-transformers

## Installation

1. Install PostgreSQL and pgvector extension:
   ```bash
   # For Debian/Ubuntu
   sudo apt install postgresql postgresql-contrib
   
   # For macOS with Homebrew
   brew install postgresql
   ```

2. Install pgvector extension:
   ```bash
   # Clone pgvector repository
   git clone https://github.com/pgvector/pgvector.git
   
   # Build and install
   cd pgvector
   make
   make install
   ```

3. Create database and enable extension:
   ```bash
   # Create database
   createdb coc_db
   
   # Connect to database
   psql coc_db
   
   # Enable pgvector extension
   CREATE EXTENSION vector;
   ```

4. Install Python dependencies:
   ```bash
   pip install psycopg2-binary numpy pypdf sentence-transformers
   ```

## Usage

### Processing PDF Files

To process all PDF files in the `split_rules` directory:

```bash
python pgvector_storage.py
```

This will:
1. Extract text from each PDF file
2. Split text into manageable chunks
3. Generate embeddings for each chunk
4. Store the content and embeddings in PostgreSQL

### Searching for Content

You can use the `PGVectorStorage` class in your Python code to search for content:

```python
from pgvector_storage import PGVectorStorage

# Initialize storage
storage = PGVectorStorage()

# Search in a specific document
results = storage.search_document(
    document_name="investigator.pdf", 
    query="How to create a character?",
    limit=5
)

# Print results
for result in results:
    print(f"Page {result['page']}: {result['content'][:100]}...")
    print(f"Similarity: {result['similarity']:.4f}")
    print("---")

# Search across all documents
all_results = storage.search_all_documents(
    query="Sanity loss mechanics",
    limit=3
)

# Print results from all documents
for doc_name, doc_results in all_results.items():
    print(f"\n== Results from {doc_name} ==")
    for result in doc_results:
        print(f"Page {result['page']}: {result['content'][:100]}...")
        print(f"Similarity: {result['similarity']:.4f}")
        print("---")
```

## Configuration

You can customize the PGVectorStorage class by providing these parameters:

- `host`: PostgreSQL host (default: "localhost")
- `port`: PostgreSQL port (default: 5432)
- `dbname`: Database name (default: "coc_db")
- `user`: Database user (default: "postgres")
- `password`: Database password (default: "postgres")
- `embedding_model`: Model name for sentence embeddings (default: "all-mpnet-base-v2")
- `chunk_size`: Number of characters per text chunk (default: 500)

Example with custom configuration:

```python
storage = PGVectorStorage(
    host="localhost",
    port=5432,
    dbname="my_coc_db",
    user="myuser",
    password="mypassword",
    embedding_model="all-MiniLM-L6-v2",
    chunk_size=800
)
```

## Database Schema

Each document is stored in its own table under the `coc_rules` schema:

- Table name: Based on the PDF filename (e.g., "investigator")
- Columns:
  - `id`: Serial primary key
  - `page`: Page number in the original PDF
  - `chunk_index`: Index of the chunk within the page
  - `content`: Text content
  - `embedding`: Vector representation of the content

Each table includes a vector index for fast similarity search using cosine similarity. 